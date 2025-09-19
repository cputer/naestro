from pathlib import Path

import yaml


CONFIG_PATH = Path("configs/evaluators/agent_companion.yaml")


def _load_config() -> dict:
    assert CONFIG_PATH.exists(), f"Config file not found: {CONFIG_PATH}"
    return yaml.safe_load(CONFIG_PATH.read_text())


def test_agent_companion_config_disabled():
    config = _load_config()
    agent_companion = config["agent_companion"]

    assert agent_companion["enabled"] is False
    assert isinstance(agent_companion.get("summary"), str)


def test_agent_companion_suites_structure():
    config = _load_config()
    suites = config["agent_companion"]["suites"]

    expected_suites = {"reasoning", "tool_use"}
    assert set(suites.keys()) == expected_suites

    for name, suite in suites.items():
        assert suite["enabled"] is False, f"Suite '{name}' should be disabled by default"
        assert isinstance(suite.get("description"), str) and suite["description"].strip()
        notes = suite.get("notes")
        assert isinstance(notes, list) and notes, f"Suite '{name}' needs non-empty notes"

        metrics = suite.get("metrics")
        assert isinstance(metrics, list) and metrics, f"Suite '{name}' must define metrics"
        assert all(isinstance(metric, str) and metric for metric in metrics)

        datasets = suite.get("datasets")
        assert isinstance(datasets, list) and datasets, f"Suite '{name}' requires datasets"
        for dataset in datasets:
            assert isinstance(dataset, dict)
            dataset_id = dataset.get("id")
            assert isinstance(dataset_id, str) and dataset_id.startswith(
                "kaggle://"
            ), f"Suite '{name}' dataset must reference a Kaggle identifier"
            split = dataset.get("split")
            assert isinstance(split, str) and split, f"Suite '{name}' dataset missing split"
            url = dataset.get("url")
            assert isinstance(url, str) and url.startswith("https://")

        assert suite.get("deterministic") is False
