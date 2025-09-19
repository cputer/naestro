from pathlib import Path

import yaml


CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs" / "policy" / "rllm.yaml"


def test_rllm_config_disabled_by_default() -> None:
    config = yaml.safe_load(CONFIG_PATH.read_text())
    assert config, "RLLM configuration should not be empty"
    assert "rllm" in config, "RLLM configuration block missing"

    rllm_config = config["rllm"]
    assert isinstance(rllm_config, dict)
    assert rllm_config.get("enabled") is False
