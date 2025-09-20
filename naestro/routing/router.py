"""Task aware router for selecting model profiles."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from naestro.routing.registry import ModelProfile, ModelRegistry


@dataclass(slots=True)
class RoutingRequest:
    task: str
    required_capabilities: frozenset[str]
    weights: dict[str, float] = field(
        default_factory=lambda: {"quality": 0.6, "latency": 0.2, "cost": 0.2}
    )


class Router:
    def __init__(self, registry: ModelRegistry) -> None:
        self._registry = registry

    def available_models(self) -> List[ModelProfile]:
        return self._registry.list()

    def select_model(self, request: RoutingRequest) -> ModelProfile:
        candidates: List[ModelProfile] = []
        for profile in self._registry.list():
            if request.required_capabilities.issubset(profile.capabilities):
                candidates.append(profile)
        if not candidates:
            raise ValueError("No model satisfies requested capabilities")
        best = max(candidates, key=lambda profile: profile.score(request.weights))
        return best


__all__ = ["Router", "RoutingRequest"]
