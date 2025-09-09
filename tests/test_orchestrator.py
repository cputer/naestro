import importlib
import logging
import os
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


def test_run_memory_error_reroutes(orch_module, monkeypatch):
    monkeypatch.setenv("SLM_BASE_URL", "http://slm")
    app = orch_module.app
    workflow_app = orch_module.workflow_app

    def raise_mem(_state):
        raise MemoryError

    monkeypatch.setattr(workflow_app, "invoke", raise_mem)
    called = {"flag": False}

    def fake_oom_guard():
        called["flag"] = True
        return True

    monkeypatch.setattr(orch_module, "oom_guard", fake_oom_guard)
    client = TestClient(app)
    resp = client.post("/run", json={"input": "hello"})
    assert resp.status_code == 500
    assert resp.json()["detail"] == "Rerouted to cloud due to OOM"
    assert called["flag"]


def test_run_no_model_endpoints(orch_module, monkeypatch):
    monkeypatch.delenv("SLM_BASE_URL", raising=False)
    monkeypatch.delenv("VLLM_BASE_URL", raising=False)
    monkeypatch.delenv("NIM_BASE_URL", raising=False)
    app = orch_module.app
    client = TestClient(app)
    resp = client.post("/run", json={"input": "hello"})
    assert resp.status_code == 500
    assert resp.json()["detail"] == "No model endpoints configured"


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


def test_thermal_guard_triggers(orch_module, monkeypatch, caplog):
    dummy_psutil = types.SimpleNamespace(
        sensors_temperatures=lambda: {"cpu": [types.SimpleNamespace(current=80)]}
    )
    monkeypatch.setitem(sys.modules, "psutil", dummy_psutil)
    monkeypatch.setenv("THERMAL_GUARD_MAX_C", "78")
    with caplog.at_level(logging.WARNING):
        assert orch_module.thermal_guard()
    assert "Thermal guard triggered" in caplog.text


def test_oom_guard_triggers(orch_module, monkeypatch, caplog):
    dummy_psutil = types.SimpleNamespace(
        virtual_memory=lambda: types.SimpleNamespace(available=50 * 1024 * 1024)
    )
    monkeypatch.setitem(sys.modules, "psutil", dummy_psutil)
    monkeypatch.setenv("OOM_GUARD_MIN_AVAILABLE_MB", "100")
    with caplog.at_level(logging.ERROR):
        assert orch_module.oom_guard()
    assert "OOM guard activated" in caplog.text


def test_backpressure_guard_triggers(orch_module, monkeypatch, caplog):
    monkeypatch.setenv("BACKPRESSURE_P95_THRESHOLD_MS", "500")
    with caplog.at_level(logging.INFO):
        assert orch_module.backpressure_guard(600)
    assert "Backpressure guard engaged" in caplog.text


def test_orchestrator_import_without_nltk(monkeypatch):
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

    real_import = importlib.import_module

    def fake_import(name, *a, **k):
        if name == "nltk":
            raise ModuleNotFoundError("No module named 'nltk'")
        return real_import(name, *a, **k)

    monkeypatch.setattr(importlib, "import_module", fake_import)
    monkeypatch.delitem(sys.modules, "nltk", raising=False)

    module = importlib.reload(importlib.import_module("src.orchestrator.orchestrator"))
    assert module is not None


def test_ensure_nltk_data_missing(monkeypatch):
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

    class DummyNltk:
        class data:
            @staticmethod
            def find(path):
                raise LookupError("missing")

        @staticmethod
        def download(*a, **k):
            return None

    orch._real_nltk = None
    orch.nltk = orch._NLTKShim()
    monkeypatch.setattr(orch.importlib, "import_module", lambda name: DummyNltk)
    with pytest.raises(LookupError) as exc:
        orch.ensure_nltk_data()
    msg = str(exc.value)
    assert "Missing NLTK corpora" in msg
    assert "punkt" in msg and "averaged_perceptron_tagger" in msg


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


def test_verify_fn_missing_flake8(monkeypatch):
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

    def fake_run(*a, **k):
        raise FileNotFoundError

    monkeypatch.setattr(orch.subprocess, "run", fake_run)
    removed = {"path": None}
    real_unlink = orch.os.unlink

    def fake_unlink(p):
        removed["path"] = p
        real_unlink(p)

    monkeypatch.setattr(orch.os, "unlink", fake_unlink)

    result = orch.verify_fn({"code": "print('hi')"})
    assert result["lint_delta"] == 0.0
    assert removed["path"] is not None
    assert not os.path.exists(removed["path"])


def test_refine_fn_missing_black(monkeypatch):
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

    def fake_run(*a, **k):
        raise FileNotFoundError

    monkeypatch.setattr(orch.subprocess, "run", fake_run)
    result = orch.refine_fn({"code": "x=1"})
    assert result["code"] == "x=1"
