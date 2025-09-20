"""Model registry definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping


@dataclass(slots=True)
class ModelProfile:
    name: str
    provider: str
    capabilities: frozenset[str]
    quality: float
    latency: float
    cost: float
    metadata: Mapping[str, object] = field(default_factory=dict)

    def score(self, weights: Mapping[str, float]) -> float:
        return (
            self.quality * weights.get("quality", 0.0)
            - self.latency * weights.get("latency", 0.0)
            - self.cost * weights.get("cost", 0.0)
        )


class ModelRegistry:
    def __init__(self, profiles: Iterable[ModelProfile] | None = None) -> None:
        self._profiles: Dict[str, ModelProfile] = {}
        if profiles is not None:
            for profile in profiles:
                self.register(profile)

    def register(self, profile: ModelProfile) -> None:
        self._profiles[profile.name] = profile

    def get(self, name: str) -> ModelProfile:
        try:
            return self._profiles[name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"Unknown model '{name}'") from exc

    def list(self) -> List[ModelProfile]:
        return list(self._profiles.values())

    def clear(self) -> None:
        self._profiles.clear()


__all__ = ["ModelProfile", "ModelRegistry"]
