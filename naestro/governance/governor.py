"""Lightweight governance layer for validating pipeline decisions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Mapping, Sequence

from naestro.core.bus import MessageBus

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from naestro.governance.policies import Policy, PolicyResult


@dataclass(slots=True)
class Decision:
    subject: str
    score: float
    metadata: Mapping[str, object] = field(default_factory=dict)

    def describe(self) -> str:
        return f"Decision(subject={self.subject!r}, score={self.score})"


class Governor:
    """Evaluates decisions against a set of registered policies."""

    def __init__(
        self,
        policies: Sequence["Policy"] | None = None,
        *,
        bus: MessageBus | None = None,
    ) -> None:

        self._policies: List[Policy] = list(policies or [])
        self._bus = bus or MessageBus()

    def register(self, policy: "Policy") -> None:
        self._policies.append(policy)

    def clear(self) -> None:
        self._policies.clear()

    def evaluate(self, decision: Decision) -> List["PolicyResult"]:

        results: List[PolicyResult] = []
        for policy in self._policies:
            results.append(policy.evaluate(decision))
        return results

    def enforce(self, decision: Decision) -> tuple[bool, List["PolicyResult"]]:
        results = self.evaluate(decision)
        allowed = all(result.passed for result in results)
        payload = {
            "decision": decision.describe(),
            "results": [
                {
                    "policy": result.name,
                    "passed": result.passed,
                    "reason": result.reason,
                }
                for result in results
            ],
        }
        self._bus.publish("governor.evaluated", payload)
        return allowed, results


__all__ = ["Decision", "Governor"]
