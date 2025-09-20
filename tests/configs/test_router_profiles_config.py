from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_PATH = Path("configs/router_profiles.yaml")


EXPECTED_MODELS = [
    {
        "name": "foundational-small",
        "provider": "naestro",
        "capabilities": ["chat", "analysis"],
        "quality": 0.7,
        "latency": 0.2,
        "cost": 0.1,
    },
    {
        "name": "foundational-pro",
        "provider": "naestro",
        "capabilities": ["chat", "analysis", "math"],
        "quality": 0.9,
        "latency": 0.4,
        "cost": 0.3,
    },
    {
        "name": "specialist-coder",
        "provider": "partner",
        "capabilities": ["code", "analysis"],
        "quality": 0.85,
        "latency": 0.3,
        "cost": 0.25,
    },
]


def test_router_profiles_config_matches_prompt() -> None:
    data = yaml.safe_load(CONFIG_PATH.read_text())
    assert data == {"models": EXPECTED_MODELS}
