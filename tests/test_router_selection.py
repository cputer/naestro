from __future__ import annotations

from pathlib import Path
from sys import path as sys_path

import pytest

if __package__ in {None, ""}:
    sys_path.append(str(Path(__file__).resolve().parents[1]))

from naestro.routing.model_registry import ModelInfo
from naestro.routing.router import ModelRouter


def test_router_ranks_models_and_applies_constraints() -> None:
    models = [
        ModelInfo(
            name="balanced",
            provider="demo",
            capabilities=frozenset({"chat", "analysis"}),
            quality=0.82,
            latency=0.3,
            cost=0.2,
        ),
        ModelInfo(
            name="high_quality",
            provider="demo",
            capabilities=frozenset({"analysis"}),
            quality=0.9,
            latency=0.35,
            cost=0.25,
        ),
        ModelInfo(
            name="fast",
            provider="demo",
            capabilities=frozenset({"chat", "analysis"}),
            quality=0.75,
            latency=0.1,
            cost=0.18,
        ),
    ]
    router = ModelRouter(models)

    base_spec = {
        "task": "analysis",
        "required_capabilities": {"analysis"},
    }
    ranked = router.rank_models(base_spec)
    assert [model.name for model in ranked] == [
        "high_quality",
        "fast",
        "balanced",
    ]

    latency_weighted = {
        "task": "analysis",
        "required_capabilities": {"analysis"},
        "weights": {"quality": 0.4, "latency": 0.5, "cost": 0.1},
    }
    latency_ranked = router.rank_models(latency_weighted)
    assert latency_ranked[0].name == "fast"

    selected = router.select_model(
        {
            "task": "analysis",
            "required_capabilities": {"analysis"},
            "exclude": {"high_quality"},
            "max_cost": 0.2,
            "max_latency": 0.3,
            "min_quality": 0.75,
        }
    )
    assert selected.name == "fast"

    with pytest.raises(ValueError):
        router.select_model({"task": "vision", "required_capabilities": {"vision"}})
