from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro.routing import BaseTaskSpec, ModelInfo, ModelRouter


def test_router_selects_best_model() -> None:
    models = [
        ModelInfo(
            name="a",
            provider="test",
            capabilities=frozenset({"chat"}),
            quality=0.6,
            latency=0.2,
            cost=0.1,
        ),
        ModelInfo(
            name="b",
            provider="test",
            capabilities=frozenset({"chat", "analysis"}),
            quality=0.9,
            latency=0.3,
            cost=0.2,
        ),
    ]
    router = ModelRouter(models)
    request: BaseTaskSpec = {
        "task": "analysis",
        "required_capabilities": {"analysis"},
    }
    selected = router.select_model(request)
    assert selected.name == "b"
