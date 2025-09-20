from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_PATH = Path("configs/trading_demo.yaml")


def test_trading_demo_config_matches_prompt() -> None:
    data = yaml.safe_load(CONFIG_PATH.read_text())
    assert data == {
        "signal_window": 3,
        "max_exposure": 1,
        "min_confidence": 0.2,
        "risk_policies": {
            "max_drawdown": 2.0,
            "min_return": 0.5,
        },
    }
