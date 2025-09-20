"""Showcase the routing registry selecting an appropriate model."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro.routing import ModelProfile, ModelRegistry, Router, RoutingRequest


def build_registry() -> ModelRegistry:
    return ModelRegistry(
        [
            ModelProfile(
                name="foundational-small",
                provider="naestro",
                capabilities=frozenset({"chat", "analysis"}),
                quality=0.7,
                latency=0.2,
                cost=0.1,
            ),
            ModelProfile(
                name="foundational-pro",
                provider="naestro",
                capabilities=frozenset({"chat", "analysis", "math"}),
                quality=0.9,
                latency=0.4,
                cost=0.3,
            ),
            ModelProfile(
                name="specialist-coder",
                provider="partner",
                capabilities=frozenset({"code", "analysis"}),
                quality=0.85,
                latency=0.3,
                cost=0.25,
            ),
        ]
    )


def main() -> None:
    registry = build_registry()
    router = Router(registry)
    request = RoutingRequest(
        task="code-review",
        required_capabilities=frozenset({"analysis", "code"}),
        weights={"quality": 0.7, "latency": 0.1, "cost": 0.2},
    )
    selected = router.select_model(request)
    print("Available models:")
    for profile in router.available_models():
        print(f"  {profile.name} -> score {profile.score(request.weights):.3f}")
    print("Selected model:", selected.name)


if __name__ == "__main__":
    main()
