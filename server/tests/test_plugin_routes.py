import importlib
import sys
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _reload_plugins_module():
    return importlib.reload(importlib.import_module("api.routes.plugins"))


def _client():
    module = importlib.reload(importlib.import_module("server.main"))
    return TestClient(module.app)


def test_deepcode_route_disabled_returns_503():
    _reload_plugins_module()
    client = _client()
    response = client.post("/plugins/deepcode/build", json={"source": {"branch": "main"}})
    assert response.status_code == 503
    assert response.json() == {"detail": "DeepCode plugin is disabled"}


def test_deepcode_route_enabled(tmp_path, monkeypatch):
    module = _reload_plugins_module()
    config_path = tmp_path / "plugins.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "plugins": {
                    "deepcode": {
                        "enabled": True,
                        "repo_dir": "/tmp/project",
                        "notes": "testing",
                    }
                }
            }
        )
    )
    monkeypatch.setattr(module, "CONFIG_PATH", config_path)
    client = _client()

    payload = {"source": {"commit": "abc123"}}
    response = client.post("/plugins/deepcode/build", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "not_wired"
    assert body["message"] == "DeepCode adapter is not wired yet"
    assert body["source"] == payload["source"]
