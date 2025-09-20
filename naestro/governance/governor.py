"""Lightweight governance layer for validating pipeline decisions."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping, MutableSequence, Sequence
from copy import deepcopy
from typing import Any

from naestro.core.bus import MessageBus

from .policies import PolicyLike


class _NullBus:
    """Fallback bus used when :mod:`jsonschema` is not available."""

    def publish(self, event: str, payload: Mapping[str, Any]) -> None:  # pragma: no cover - trivial
        return None

from .schemas import Decision, PolicyInput, PolicyPatch


def _coerce_input(data: PolicyInput | Mapping[str, Any]) -> PolicyInput:
    if isinstance(data, PolicyInput):
        return data.model_copy(deep=True)
    return PolicyInput.model_validate(data)


class Governor:
    """Evaluates inputs against a set of registered policies."""

    def __init__(
        self,
        policies: Sequence[PolicyLike] | None = None,
        *,
        bus: MessageBus | None = None,
    ) -> None:
        self._policies: list[PolicyLike] = list(policies or [])
        if bus is not None:
            self._bus = bus
        else:
            try:
                self._bus = MessageBus()
            except RuntimeError:
                self._bus = _NullBus()

    def register(self, policy: PolicyLike) -> None:
        self._policies.append(policy)

    def clear(self) -> None:
        self._policies.clear()

    def evaluate(
        self, data: PolicyInput | Mapping[str, Any]
    ) -> list[Decision]:
        policy_input = _coerce_input(data)
        return [policy.evaluate(policy_input) for policy in self._policies]

    def enforce(
        self,
        data: PolicyInput | Mapping[str, Any],
        *,
        apply_policy_patches: bool = False,
        return_input: bool = False,
    ) -> tuple[bool, list[Decision]] | tuple[bool, list[Decision], PolicyInput]:
        policy_input = _coerce_input(data)
        plan = deepcopy(policy_input.plan)
        results: list[Decision] = []
        for policy in self._policies:
            decision = policy.evaluate(policy_input)
            results.append(decision)
            if apply_policy_patches and decision.patches:
                plan = apply_patches(plan, decision.patches)
                policy_input.plan = plan
        allowed = all(result.passed for result in results)
        payload = {
            "input": policy_input.model_dump(),
            "results": [result.model_dump() for result in results],
            "approved": allowed,
        }
        self._bus.publish("governor.evaluated", payload)
        if return_input:
            return allowed, results, policy_input
        return allowed, results


def _ensure_container(
    container: Any,
    key: str | int,
    *,
    create: bool,
) -> Any:
    if isinstance(key, int):
        if not isinstance(container, MutableSequence):
            raise TypeError("Expected a sequence for integer path segments")
        if key >= len(container):
            if not create:
                raise IndexError(f"Index {key} out of range for patch path")
            while len(container) <= key:
                container.append({})
        return container[key]
    if not isinstance(container, MutableMapping):
        raise TypeError("Expected a mapping for string path segments")
    if key not in container:
        if not create:
            raise KeyError(f"Missing key {key!r} in patch path")
        container[key] = {}
    return container[key]


def _assign(container: Any, key: str | int, value: Any) -> None:
    if isinstance(key, int):
        if not isinstance(container, MutableSequence):
            raise TypeError("Expected a sequence for integer assignment")
        if key == len(container):
            container.append(value)
            return
        if key >= len(container):
            raise IndexError(f"Index {key} out of range for assignment")
        container[key] = value
        return
    if not isinstance(container, MutableMapping):
        raise TypeError("Expected a mapping for string assignment")
    container[key] = value


def _remove(container: Any, key: str | int) -> None:
    if isinstance(key, int):
        if not isinstance(container, MutableSequence):
            raise TypeError("Expected a sequence for integer removal")
        if not (-len(container) <= key < len(container)):
            raise IndexError(f"Index {key} out of range for removal")
        del container[key]
        return
    if not isinstance(container, MutableMapping):
        raise TypeError("Expected a mapping for string removal")
    container.pop(key, None)


def apply_patches(plan: Mapping[str, Any], patches: Iterable[PolicyPatch]) -> dict[str, Any]:
    """Apply a collection of declarative patches to the supplied plan."""

    result: Any = deepcopy(plan)
    for patch in patches:
        path = list(patch.get("path", ()))
        if not path:
            raise ValueError("Patch operations require a non-empty path")
        op = patch.get("op", "set")
        value = deepcopy(patch.get("value")) if "value" in patch else None
        current = result
        for segment in path[:-1]:
            current = _ensure_container(current, segment, create=op in {"set", "merge"})
        final_segment = path[-1]
        if op == "set":
            _assign(current, final_segment, value)
        elif op == "remove":
            _remove(current, final_segment)
        elif op == "merge":
            target = _ensure_container(current, final_segment, create=True)
            if not isinstance(target, MutableMapping):
                raise TypeError("Merge operations require a mapping target")
            if value is None:
                continue
            if not isinstance(value, Mapping):
                raise TypeError("Merge values must be mappings")
            target.update(value)
        else:  # pragma: no cover - defensive programming
            raise ValueError(f"Unsupported patch operation: {op!r}")
    if isinstance(result, MutableMapping):
        return dict(result)
    return result


__all__ = ["Decision", "Governor", "PolicyInput", "PolicyPatch", "apply_patches"]
