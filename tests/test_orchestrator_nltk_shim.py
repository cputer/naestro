import importlib
import sys
import types

import pytest


def _setup_dummy_langgraph(monkeypatch):
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


def test_nltk_shim_triggers_download(monkeypatch):
    _setup_dummy_langgraph(monkeypatch)

    real_import = importlib.import_module

    def fake_import(name, *a, **k):
        if name == "nltk":
            raise ModuleNotFoundError
        return real_import(name, *a, **k)

    monkeypatch.setattr(importlib, "import_module", fake_import)
    monkeypatch.delitem(sys.modules, "nltk", raising=False)

    orch = importlib.reload(importlib.import_module("src.orchestrator.orchestrator"))

    calls = []

    def fake_download(pkg, *a, **k):
        calls.append(pkg)

    monkeypatch.setattr(orch.nltk, "download", fake_download)

    with pytest.raises(LookupError):
        orch.ensure_nltk_data()

    assert set(calls) == {"punkt", "averaged_perceptron_tagger"}


def test_nltk_real_module(monkeypatch):
    _setup_dummy_langgraph(monkeypatch)

    fake_nltk = types.SimpleNamespace(downloads=[])

    def download(pkg, *a, **k):
        fake_nltk.downloads.append(pkg)

    fake_nltk.download = download
    fake_nltk.data = types.SimpleNamespace(find=lambda path: True)

    monkeypatch.setitem(sys.modules, "nltk", fake_nltk)

    orch = importlib.reload(importlib.import_module("src.orchestrator.orchestrator"))

    assert orch.ensure_nltk_real() is True
    assert orch.ensure_nltk_data() is fake_nltk
    assert fake_nltk.downloads == []
