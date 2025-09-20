from __future__ import annotations

from naestro.routing import ModelProfile, ModelRegistry, Router, RoutingRequest


def test_router_selects_best_model() -> None:
    registry = ModelRegistry(
        [
            ModelProfile(
                name="a",
                provider="test",
                capabilities=frozenset({"chat"}),
                quality=0.6,
                latency=0.2,
                cost=0.1,
            ),
            ModelProfile(
                name="b",
                provider="test",
                capabilities=frozenset({"chat", "analysis"}),
                quality=0.9,
                latency=0.3,
                cost=0.2,
            ),
        ]
    )
    router = Router(registry)
    request = RoutingRequest(
        task="analysis", required_capabilities=frozenset({"analysis"})
    )
    selected = router.select_model(request)
    assert selected.name == "b"
