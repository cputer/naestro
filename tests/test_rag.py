import importlib
import sys
import types
from types import SimpleNamespace

import pytest


@pytest.fixture
def rag(monkeypatch):
    """Import src.rag with external dependencies mocked."""
    # Dummy sentence transformer
    dummy_model = SimpleNamespace(encode=lambda text: [0.1, 0.2])
    st_module = types.ModuleType("sentence_transformers")
    st_module.SentenceTransformer = lambda *a, **k: dummy_model
    monkeypatch.setitem(sys.modules, "sentence_transformers", st_module)

    # Dummy psycopg2 modules
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
    rag.model = dummy_model
    return rag


def test_init_connection_pool(rag, monkeypatch):
    rag.pool = None

    class DummyPool:
        def __init__(self, minc, maxc, dsn):
            self.args = (minc, maxc, dsn)

    monkeypatch.setattr(rag, "SimpleConnectionPool", DummyPool)
    pool = rag.init_connection_pool(dsn="db://", minconn=1, maxconn=2)
    assert isinstance(pool, DummyPool)
    assert pool.args == (1, 2, "db://")
    assert rag.pool is pool


def test_insert_embedding_success(rag):
    class DummyCursor:
        def execute(self, q, params):
            self.executed = (q, params)

        def fetchone(self):
            return (5,)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    class DummyConn:
        def __init__(self):
            self.cur = DummyCursor()
            self.committed = False

        def cursor(self):
            return self.cur

        def commit(self):
            self.committed = True

        def rollback(self):
            self.rollback_called = True

    class DummyPool:
        def __init__(self):
            self.conn = DummyConn()

        def getconn(self):
            return self.conn

        def putconn(self, conn):
            self.put = conn

    rag.pool = DummyPool()
    result = rag.insert_embedding("text", [0.1])
    assert result == {"success": True, "id": 5}
    assert rag.pool.conn.committed


def test_hybrid_search(rag):
    class DummyCursor:
        def execute(self, q, params):
            self.executed = True

        def fetchall(self):
            return [(1, "row")]

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    class DummyConn:
        def __init__(self):
            self.cur = DummyCursor()

        def cursor(self):
            return self.cur

        def commit(self):
            self.committed = True

        def rollback(self):
            self.rollback_called = True

    class DummyPool:
        def __init__(self):
            self.conn = DummyConn()

        def getconn(self):
            return self.conn

        def putconn(self, conn):
            self.put = conn

    rag.pool = DummyPool()
    result = rag.hybrid_search("query")
    assert result["rows"] == [(1, "row")]


def test_update_feedback(rag):
    class DummyCursor:
        def __init__(self):
            self.rowcount = 1

        def execute(self, q, params):
            self.executed = (q, params)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    class DummyConn:
        def __init__(self):
            self.cur = DummyCursor()
            self.committed = False

        def cursor(self):
            return self.cur

        def commit(self):
            self.committed = True

        def rollback(self):
            self.rollback_called = True

    class DummyPool:
        def __init__(self):
            self.conn = DummyConn()

        def getconn(self):
            return self.conn

        def putconn(self, conn):
            self.put = conn

    rag.pool = DummyPool()
    result = rag.update_feedback(1, 0.2)
    assert result == {"success": True, "updated": 1}
    assert rag.pool.conn.committed

def test_insert_embedding_connection_failure(rag, monkeypatch):
    def raise_conn():
        raise RuntimeError("no connection")

    monkeypatch.setattr(rag, "_get_conn", raise_conn)
    with pytest.raises(RuntimeError):
        rag.insert_embedding("text", [0.1])


def test_hybrid_search_invalid_input(rag, monkeypatch):
    monkeypatch.setattr(rag, "_get_conn", lambda: object())

    def bad_embed(text):
        raise ValueError("invalid text")

    monkeypatch.setattr(rag, "embed_text", bad_embed)
    with pytest.raises(ValueError):
        rag.hybrid_search(None)
