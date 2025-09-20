"""Model registry definitions for routing."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, Mapping, Sequence

DEFAULT_WEIGHTS: Mapping[str, float] = {
    "quality": 0.6,
    "latency": 0.2,
    "cost": 0.2,
}


@dataclass(frozen=True, slots=True)
class ModelInfo:
    """Describes a deployable model endpoint for routing decisions."""

    name: str
    provider: str
    capabilities: frozenset[str]
    quality: float
    latency: float
    cost: float
    metadata: Mapping[str, object] = field(default_factory=dict)

    def score(self, weights: Mapping[str, float]) -> float:
        """Compute the weighted score for this model.

        Args:
            weights: Mapping with weights for ``quality``, ``latency`` and ``cost``.

        Returns:
            A floating point score where higher is better.
        """

        return (
            self.quality * weights.get("quality", 0.0)
            - self.latency * weights.get("latency", 0.0)
            - self.cost * weights.get("cost", 0.0)
        )


class ModelRegistry:
    """In-memory registry of :class:`ModelInfo` objects."""

    def __init__(self, models: Iterable[ModelInfo] | None = None) -> None:
        self._models: Dict[str, ModelInfo] = {}
        if models is not None:
            for model in models:
                self.register(model)

    def register(self, model: ModelInfo) -> None:
        """Register or update a model entry."""

        self._models[model.name] = model

    def unregister(self, name: str) -> None:
        """Remove a model from the registry if present."""

        self._models.pop(name, None)

    def get(self, name: str) -> ModelInfo:
        """Return the :class:`ModelInfo` with ``name``.

        Raises:
            KeyError: If the model is unknown.
        """

        try:
            return self._models[name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"Unknown model '{name}'") from exc

    def __contains__(self, name: str) -> bool:
        return name in self._models

    def __iter__(self) -> Iterator[ModelInfo]:
        return iter(self._models.values())

    def values(self) -> Sequence[ModelInfo]:
        return list(self._models.values())

    def clear(self) -> None:
        self._models.clear()

    def copy(self) -> "ModelRegistry":
        return ModelRegistry(self._models.values())


REGISTRY = ModelRegistry()

__all__ = ["DEFAULT_WEIGHTS", "ModelInfo", "ModelRegistry", "REGISTRY"]
