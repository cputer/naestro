import importlib
import sys
import types

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def orch_module(monkeypatch):
    dummy_workflow = types.SimpleNamespace(invoke=lambda state: state)
    dummy_orchestrator = types.SimpleNamespace(app=dummy_workflow)
    monkeypatch.setitem(
        sys.modules, "src.orchestrator.orchestrator", dummy_orchestrator
    )
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


def test_build_plan_missing_corpus(monkeypatch):
    class DummyGraph:
        def add_node(self, *a, **k):
            return None

        def add_edge(self, *a, **k):
            return None

        def add_conditional_edge(self, *a, **k):
            return None

        def compile(self):
            return None

    monkeypatch.setitem(
        sys.modules, "langgraph", types.SimpleNamespace(Graph=DummyGraph)
    )
    orch = importlib.reload(importlib.import_module("src.orchestrator.orchestrator"))

    def raise_lookup():
        raise LookupError("missing")

    monkeypatch.setattr(orch, "ensure_nltk_data", raise_lookup)
    with pytest.raises(RuntimeError, match="NLTK"):
        orch._build_plan("hello world")


def test_human_review_missing_corpus(monkeypatch):
    class DummyGraph:
        def add_node(self, *a, **k):
            return None

        def add_edge(self, *a, **k):
            return None

        def add_conditional_edge(self, *a, **k):
            return None

        def compile(self):
            return None

    monkeypatch.setitem(
        sys.modules, "langgraph", types.SimpleNamespace(Graph=DummyGraph)
    )
    orch = importlib.reload(importlib.import_module("src.orchestrator.orchestrator"))

    def raise_lookup():
        raise LookupError("missing")

    monkeypatch.setattr(orch, "ensure_nltk_data", raise_lookup)
    with pytest.raises(RuntimeError, match="NLTK"):
        orch.human_review_fn({"plan": "do thing"})
