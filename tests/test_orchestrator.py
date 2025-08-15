import importlib
import sys
import types
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def orch_module(monkeypatch):
    dummy_workflow = types.SimpleNamespace(invoke=lambda state: state)
    dummy_orchestrator = types.SimpleNamespace(app=dummy_workflow)
    monkeypatch.setitem(sys.modules, "src.orchestrator.orchestrator", dummy_orchestrator)
    module = importlib.reload(importlib.import_module("src.orchestrator.main"))
    return module


def test_health(orch_module):
    app = orch_module.app
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_run(orch_module, monkeypatch):
    monkeypatch.setenv("SLM_BASE_URL", "http://slm")
    app = orch_module.app
    workflow_app = orch_module.workflow_app
    monkeypatch.setattr(workflow_app, "invoke", lambda state: state)
    client = TestClient(app)
    resp = client.post("/run", json={"input": "hello"})
    assert resp.status_code == 200
    data = resp.json()["result"]
    assert data["input"] == "hello"
    assert data["model_url"] == "http://slm"


def test_run_unknown_policy(orch_module):
    app = orch_module.app
    client = TestClient(app)
    resp = client.post("/run", json={"input": "x", "model": "unknown"})
    assert resp.status_code == 400

def test_run_missing_input(orch_module):
    app = orch_module.app
    client = TestClient(app)
    resp = client.post("/run", json={"model": "slm"})
    assert resp.status_code == 422


def test_unknown_route(orch_module):
    app = orch_module.app
    client = TestClient(app)
    resp = client.get("/doesnotexist")
    assert resp.status_code == 404
