"""Showcase the routing registry selecting an appropriate model."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro.routing import BaseTaskSpec, ModelInfo, ModelRouter


def build_router() -> ModelRouter:
    models = [
        ModelInfo(
            name="foundational-small",
            provider="naestro",
            capabilities=frozenset({"chat", "analysis"}),
            quality=0.7,
            latency=0.2,
            cost=0.1,
        ),
        ModelInfo(
            name="foundational-pro",
            provider="naestro",
            capabilities=frozenset({"chat", "analysis", "math"}),
            quality=0.9,
            latency=0.4,
            cost=0.3,
        ),
        ModelInfo(
            name="specialist-coder",
            provider="partner",
            capabilities=frozenset({"code", "analysis"}),
            quality=0.85,
            latency=0.3,
            cost=0.25,
        ),
    ]
    return ModelRouter(models)


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
