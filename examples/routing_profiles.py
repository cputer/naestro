"""Showcase selecting an appropriate model using the router APIs."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro import BaseTaskSpec, ModelInfo, ModelRouter


CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "router_profiles.yaml"


def _load_model_profiles() -> list[ModelInfo]:
    """Load model definitions from the router profiles configuration."""

    data = yaml.safe_load(CONFIG_PATH.read_text()) or {}
    models = []
    for entry in data.get("models", []):
        models.append(
            ModelInfo(
                name=entry["name"],
                provider=entry["provider"],
                capabilities=frozenset(entry.get("capabilities", [])),
                quality=float(entry["quality"]),
                latency=float(entry["latency"]),
                cost=float(entry["cost"]),
            )
        )
    return models


def build_router() -> ModelRouter:
    """Seed the router with a few sample models."""

    return ModelRouter(_load_model_profiles())


def main() -> None:
    router = build_router()
    task: BaseTaskSpec = {
        "task": "code-review",
        "required_capabilities": {"analysis", "code"},
        "weights": {"quality": 0.7, "latency": 0.1, "cost": 0.2},
    }
    selected = router.select_model(task)
    print("Available models:")
    for model in router.available_models():
        weights = task.get("weights") or router.default_weights
        print(f"  {model.name} -> score {model.score(weights):.3f}")
    print("Selected model:", selected.name)


if __name__ == "__main__":
    main()
