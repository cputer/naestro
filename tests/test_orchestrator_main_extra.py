import importlib
import sys
import types

import pytest
from fastapi import HTTPException


@pytest.fixture
def om(monkeypatch):
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
    module = importlib.reload(importlib.import_module("src.orchestrator.main"))
    module.workflow_app = types.SimpleNamespace(invoke=lambda state: state)
    return module


def test_thermal_guard_no_trigger(om, monkeypatch):
    class DummyPsutil:
        @staticmethod
        def sensors_temperatures():
            return {"cpu": [types.SimpleNamespace(current=30)]}

    monkeypatch.setenv("THERMAL_GUARD_MAX_C", "60")
    monkeypatch.setitem(sys.modules, "psutil", DummyPsutil)
    assert om.thermal_guard() is False


def test_oom_guard_disabled(om, monkeypatch):
    monkeypatch.delenv("OOM_GUARD_MIN_AVAILABLE_MB", raising=False)
    assert om.oom_guard() is False


def test_oom_guard_sufficient_memory(om, monkeypatch):
    class DummyPsutil:
        @staticmethod
        def virtual_memory():
            return types.SimpleNamespace(available=200 * 1024 * 1024)

    monkeypatch.setenv("OOM_GUARD_MIN_AVAILABLE_MB", "100")
    monkeypatch.setitem(sys.modules, "psutil", DummyPsutil)
    assert om.oom_guard() is False


def test_route_model_auto_no_endpoints(om, monkeypatch):
    monkeypatch.delenv("SLM_BASE_URL", raising=False)
    monkeypatch.delenv("NIM_BASE_URL", raising=False)
    monkeypatch.delenv("VLLM_BASE_URL", raising=False)
    with pytest.raises(HTTPException):
        om._route_model(None)


def test_route_model_explicit(om, monkeypatch):
    monkeypatch.setenv("NIM_BASE_URL", "http://nim")
    assert om._route_model("nim") == "http://nim"


def test_run_memory_error(om, monkeypatch):
    monkeypatch.setattr(om, "_route_model", lambda policy: "url")
    called = {}
    monkeypatch.setattr(om, "oom_guard", lambda: called.setdefault("x", True))

    def raise_mem(state):
        raise MemoryError

    monkeypatch.setattr(om.workflow_app, "invoke", raise_mem)
    with pytest.raises(HTTPException) as exc:
        om.run(om.TaskRequest(input="x"))
    assert exc.value.status_code == 500
    assert called["x"]


def test_run_generic_error(om, monkeypatch):
    monkeypatch.setattr(om, "_route_model", lambda policy: "url")
    monkeypatch.setattr(
        om.workflow_app,
        "invoke",
        lambda state: (_ for _ in ()).throw(ValueError("boom")),
    )
    with pytest.raises(HTTPException) as exc:
        om.run(om.TaskRequest(input="x"))
    assert exc.value.status_code == 500


def test_math_endpoint(om, monkeypatch):
    monkeypatch.setattr(om.math_app, "invoke", lambda state: {"result": 1})
    resp = om.math(om.MathRequest(query="1+1"))
    assert resp.result["result"] == 1
