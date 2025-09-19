from pathlib import Path

import yaml

from integrations.datasets.llm_datasets_registry import LLMDatasetsRegistry


CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs" / "datasets" / "llm_datasets.yaml"


def test_llm_datasets_config_is_disabled() -> None:
    config = yaml.safe_load(CONFIG_PATH.read_text())
    assert config, "LLM datasets configuration should not be empty"
    assert "llm_datasets" in config, "llm_datasets block missing from configuration"

    llm_config = config["llm_datasets"]
    assert isinstance(llm_config, dict)
    assert llm_config.get("enabled") is False


def test_registry_reports_disabled_state() -> None:
    registry = LLMDatasetsRegistry()
    assert registry.enabled is False
    categories = registry.list_categories()
    assert isinstance(categories, list)
    assert "general_purpose" in categories
