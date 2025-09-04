import importlib
import sys
import types

import pytest


def _setup_langgraph(monkeypatch):
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


def _setup_nltk(monkeypatch):
    fake = types.SimpleNamespace()
    fake.data = types.SimpleNamespace(find=lambda path: True)
    fake.sent_tokenize = lambda text: [s for s in text.split(".") if s]
    fake.word_tokenize = lambda text: text.split()
    fake.pos_tag = lambda tokens: [(t, "VB") for t in tokens]
    monkeypatch.setitem(sys.modules, "nltk", fake)
    return fake


def _load_orch(monkeypatch):
    _setup_langgraph(monkeypatch)
    _setup_nltk(monkeypatch)
    return importlib.reload(importlib.import_module("src.orchestrator.orchestrator"))


def test_nltk_shim_download(monkeypatch):
    _setup_langgraph(monkeypatch)
    orch = importlib.reload(importlib.import_module("src.orchestrator.orchestrator"))
    assert orch._NLTKShim.download("punkt") is None


def test_build_plan_and_planner(monkeypatch):
    orch = _load_orch(monkeypatch)
    plan = orch._build_plan("Hello world.")
    assert plan.startswith("-")
    res = orch.planner_fn({"input": "Hello world."})
    assert "plan" in res and res["context_size"] == len("Hello world.")


def test_implement_and_entropy(monkeypatch):
    orch = _load_orch(monkeypatch)
    result = orch.implement_fn({"plan": "- do things"})
    assert "def do_things" in result["code"]
    assert orch._shannon_entropy("") == 0.0


def test_implement_missing_corpus(monkeypatch):
    orch = _load_orch(monkeypatch)
    monkeypatch.setattr(
        orch, "ensure_nltk_data", lambda: (_ for _ in ()).throw(LookupError("missing"))
    )
    with pytest.raises(RuntimeError):
        orch.implement_fn({"plan": "- step"})


def test_verify_fn_errors(monkeypatch):
    orch = _load_orch(monkeypatch)
    monkeypatch.setitem(
        sys.modules,
        "py_compile",
        types.SimpleNamespace(
            compile=lambda *a, **k: (_ for _ in ()).throw(Exception())
        ),
    )

    class DummyResult:
        stdout = "E1\nE2\n"

    monkeypatch.setattr(orch.subprocess, "run", lambda *a, **k: DummyResult())
    res = orch.verify_fn({"code": "bad"})
    assert res["passed"] is False
    assert res["lint_delta"] == 1 / (1 + 2)


def test_refine_fn_success(monkeypatch):
    orch = _load_orch(monkeypatch)
    monkeypatch.setattr(orch.subprocess, "run", lambda *a, **k: None)
    res = orch.refine_fn({"code": "x=1"})
    assert "x=1" in res["code"]


def test_human_review_and_conditions(monkeypatch):
    orch = _load_orch(monkeypatch)
    res = orch.human_review_fn({"plan": "run tests"})
    assert res["approved"]
    assert orch.approve_cond(res)
    assert orch.refine_gate(
        {"passed_delta": 0, "lint_delta": 0, "entropy_delta": 0, "budget": 1.0}
    )
