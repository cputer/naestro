import importlib
import sys
import types
from types import SimpleNamespace

import pytest


@pytest.fixture
def rag(monkeypatch):
    """Import src.rag with external dependencies mocked."""
    dummy_model = SimpleNamespace(encode=lambda text: [0.1, 0.2])
    st_module = types.ModuleType("sentence_transformers")
    st_module.SentenceTransformer = lambda *a, **k: dummy_model
    monkeypatch.setitem(sys.modules, "sentence_transformers", st_module)

    pool_module = types.ModuleType("psycopg2.pool")

    class DummySimpleConnectionPool:
        def __init__(self, minconn, maxconn, dsn):
            pass

    pool_module.SimpleConnectionPool = DummySimpleConnectionPool
    psycopg2_module = types.ModuleType("psycopg2")
    psycopg2_module.pool = pool_module
    monkeypatch.setitem(sys.modules, "psycopg2", psycopg2_module)
    monkeypatch.setitem(sys.modules, "psycopg2.pool", pool_module)

    rag = importlib.reload(importlib.import_module("src.rag"))
    rag.model = None
    rag.pool = None
    return rag


def test_init_model_twice(rag):
    m1 = rag.init_model()
    m2 = rag.init_model()
    assert m1 is not None
    assert m1 is m2


def test_init_connection_pool_twice(rag):
    pool1 = rag.init_connection_pool(dsn="db://", minconn=1, maxconn=2)
    pool2 = rag.init_connection_pool(dsn="db://", minconn=1, maxconn=2)
    assert pool1 is not None
    assert pool1 is pool2
