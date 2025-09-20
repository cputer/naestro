from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_PATH = Path("configs/policies_basic.yaml")


EXPECTED_POLICIES = {
    "max_drawdown": 2.0,
    "min_return": 0.5,
}


def test_policies_basic_config_matches_prompt() -> None:
    data = yaml.safe_load(CONFIG_PATH.read_text())
    assert data == {"policies": EXPECTED_POLICIES}
