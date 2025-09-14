import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Ensure repository root is on sys.path for imports when tests are executed from
# within this subdirectory.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _get_client():
    module = importlib.reload(importlib.import_module("server.main"))
    return TestClient(module.app)


def test_get_default_preferences():
    client = _get_client()
    resp = client.get("/orchestrator/prefs")
    assert resp.status_code == 200
    assert resp.json() == {}


def test_set_and_get_preferences():
    client = _get_client()
    data = {"example": "value", "flag": True}
    resp = client.post("/orchestrator/prefs", json=data)
    assert resp.status_code == 200
    assert resp.json() == data

    resp = client.get("/orchestrator/prefs")
    assert resp.status_code == 200
    assert resp.json() == data
