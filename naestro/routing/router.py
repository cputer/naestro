"""Task aware router for selecting the best model profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence, cast

from .model_registry import DEFAULT_WEIGHTS, REGISTRY, ModelInfo, ModelRegistry
from .task_specs import BaseTaskSpec, ChatTaskSpec, TaskSpec, ToolTaskSpec

TaskConfiguration = BaseTaskSpec | TaskSpec | ChatTaskSpec | ToolTaskSpec


def _as_mapping(spec: TaskConfiguration) -> Mapping[str, Any]:
    return cast(Mapping[str, Any], spec)


@dataclass
class ModelRouter:
    """Select models from a :class:`ModelRegistry` given a task specification."""

    registry: ModelRegistry
    default_weights: Mapping[str, float]

    def __init__(
        self,
        registry: ModelRegistry | Iterable[ModelInfo] | None = None,
        *,
        default_weights: Mapping[str, float] | None = None,
    ) -> None:
        if registry is None:
            self.registry = REGISTRY.copy()
        elif isinstance(registry, ModelRegistry):
            self.registry = registry
        else:
            self.registry = ModelRegistry(registry)
        self.default_weights = dict(default_weights or DEFAULT_WEIGHTS)

    def available_models(self) -> Sequence[ModelInfo]:
        """Return all registered models."""

        return list(self.registry)

    def register_model(self, model: ModelInfo) -> None:
        """Add a model to the underlying registry."""

        self.registry.register(model)

    def select_model(self, spec: TaskConfiguration) -> ModelInfo:
        """Select the highest scoring model for ``spec``.

        Raises:
            ValueError: If no candidate satisfies the constraints.
        """

        ranked = self.rank_models(spec)
        if not ranked:
            task = _as_mapping(spec).get("task", "<unknown>")
            raise ValueError(
                f"No model satisfies requested capabilities for task '{task}'"
            )
        return ranked[0]

    def rank_models(self, spec: TaskConfiguration) -> list[ModelInfo]:
        """Return all matching models sorted from best to worst."""

        data = _as_mapping(spec)
        required = self._normalise_capabilities(data["required_capabilities"])
        weights = self._resolve_weights(data)
        excluded = {name for name in self._iterable_of_strings(data.get("exclude"))}
        min_quality = self._optional_float(data.get("min_quality"))
        max_latency = self._optional_float(data.get("max_latency"))
        max_cost = self._optional_float(data.get("max_cost"))

        scored: list[tuple[float, ModelInfo]] = []
        for model in self.registry:
            if excluded and model.name in excluded:
                continue
            if not required.issubset(model.capabilities):
                continue
            if min_quality is not None and model.quality < min_quality:
                continue
            if max_latency is not None and model.latency > max_latency:
                continue
            if max_cost is not None and model.cost > max_cost:
                continue
            scored.append((model.score(weights), model))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [model for _, model in scored]

    @staticmethod
    def _normalise_capabilities(values: object) -> frozenset[str]:
        if values is None:
            return frozenset()
        if isinstance(values, frozenset):
            return values
        if isinstance(values, set):
            return frozenset(values)
        if isinstance(values, (list, tuple)):
            return frozenset(str(value) for value in values)
        raise TypeError("required_capabilities must be a collection of strings")

    def _resolve_weights(self, data: Mapping[str, Any]) -> Mapping[str, float]:
        custom = data.get("weights")
        if not custom:
            return dict(self.default_weights)
        weights = dict(self.default_weights)
        weights.update(custom)
        return weights

    @staticmethod
    def _iterable_of_strings(values: object) -> Sequence[str]:
        if values is None:
            return ()
        if isinstance(values, (set, frozenset, list, tuple)):
            return [str(value) for value in values]
        raise TypeError("exclude must be a collection of model names if provided")

    @staticmethod
    def _optional_float(value: object) -> float | None:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        raise TypeError("constraint values must be numeric if provided")


class RoutePolicy:
    """Callable wrapper around :class:`ModelRouter` for policy-based routing."""

    def __init__(
        self,
        registry: ModelRegistry | Iterable[ModelInfo] | None = None,
        *,
        default_weights: Mapping[str, float] | None = None,
    ) -> None:
        self.router = ModelRouter(registry, default_weights=default_weights)

    def __call__(self, spec: TaskConfiguration) -> ModelInfo:
        """Select the best model for ``spec``."""

        return self.router.select_model(spec)

    def rank(self, spec: TaskConfiguration) -> list[ModelInfo]:
        """Return the ranked candidates for ``spec``."""

        return self.router.rank_models(spec)


__all__ = ["ModelRouter", "RoutePolicy"]
