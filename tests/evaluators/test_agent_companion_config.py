from pathlib import Path

import yaml


CONFIG_PATH = Path("configs/evaluators/agent_companion.yaml")


def test_agent_companion_config_disabled():
    assert CONFIG_PATH.exists(), f"Config file not found: {CONFIG_PATH}"

    config = yaml.safe_load(CONFIG_PATH.read_text())

    assert config["agent_companion"]["enabled"] is False
