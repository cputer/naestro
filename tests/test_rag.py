import importlib
import sys
import threading
import time
import types
from contextlib import contextmanager
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
        def __init__(self, dsn, minc, maxc):
            self.args = (dsn, minc, maxc)

    monkeypatch.setattr(rag, "ConnectionPool", DummyPool)
    pool = rag.init_connection_pool(dsn="db://", minconn=1, maxconn=2)
    assert isinstance(pool, DummyPool)
    assert pool.args == ("db://", 1, 2)
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

        @contextmanager
        def connection(self):
            yield self.conn

    rag.pool = DummyPool()
    result = rag.insert_embedding("text", [0.1])
    assert isinstance(result, rag.InsertEmbeddingResult)
    assert result.id == 5
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

        @contextmanager
        def connection(self):
            yield self.conn

    rag.pool = DummyPool()
    result = rag.hybrid_search("query")
    assert isinstance(result, rag.HybridSearchResult)
    assert result.rows == [(1, "row")]


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

        @contextmanager
        def connection(self):
            yield self.conn

    rag.pool = DummyPool()
    result = rag.update_feedback(1, 0.2)
    assert isinstance(result, rag.UpdateFeedbackResult)
    assert result.updated == 1
    assert rag.pool.conn.committed


def test_insert_embedding_connection_failure(rag):
    class BadPool:
        def connection(self):
            raise RuntimeError("no connection")

    rag.pool = BadPool()
    with pytest.raises(RuntimeError):
        rag.insert_embedding("text", [0.1])


def test_hybrid_search_invalid_input(rag, monkeypatch):
    @contextmanager
    def fake_conn():
        yield object()

    rag.pool = SimpleNamespace(connection=fake_conn)

    def bad_embed(text):
        raise ValueError("invalid text")

    monkeypatch.setattr(rag, "embed_text", bad_embed)
    with pytest.raises(ValueError):
        rag.hybrid_search(None)


def test_connection_pool_context(rag, monkeypatch):
    class DummySP:
        def __init__(self, minconn, maxconn, dsn):
            self.conn = object()

        def getconn(self):
            return self.conn

        def putconn(self, conn):
            self.released = conn

        def closeall(self):
            self.closed = True

    monkeypatch.setattr(rag, "SimpleConnectionPool", DummySP)
    cp = rag.ConnectionPool("dsn", 1, 2)
    with cp.connection() as conn:
        assert conn is cp._pool.conn
    assert cp._pool.released is cp._pool.conn
    cp.close()
    assert cp._pool.closed


def test_init_connection_pool_requires_dsn(rag, monkeypatch):
    rag.pool = None
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValueError):
        rag.init_connection_pool()


def test_close_pool(rag):
    class DummyPool:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    dummy = DummyPool()
    rag.pool = dummy
    rag.close_pool()
    assert dummy.closed and rag.pool is None


def test_insert_embedding_pool_none(rag):
    rag.pool = None
    with pytest.raises(RuntimeError):
        rag.insert_embedding("text", [0.1])


def test_hybrid_search_pool_none(rag):
    rag.pool = None
    with pytest.raises(RuntimeError):
        rag.hybrid_search("x")


def test_update_feedback_pool_none(rag):
    rag.pool = None
    with pytest.raises(RuntimeError):
        rag.update_feedback(1)


def test_init_model_thread_safe(rag, monkeypatch):
    """Ensure only one model instance is created under concurrent calls."""
    rag.model = None

    class DummyModel:
        pass

    calls = {"count": 0}

    def dummy_constructor(*args, **kwargs):
        calls["count"] += 1
        time.sleep(0.01)
        return DummyModel()

    monkeypatch.setattr(rag, "SentenceTransformer", dummy_constructor)

    results = []

    def worker():
        results.append(rag.init_model())

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(r is results[0] for r in results)
    assert calls["count"] == 1


def test_init_connection_pool_thread_safe(rag, monkeypatch):
    """Ensure only one pool instance is created under concurrent calls."""
    rag.pool = None

    class DummyPool:
        pass

    calls = {"count": 0}

    def dummy_constructor(dsn, minconn, maxconn):
        calls["count"] += 1
        time.sleep(0.01)
        return DummyPool()

    monkeypatch.setattr(rag, "ConnectionPool", dummy_constructor)

    results = []

    def worker():
        results.append(rag.init_connection_pool(dsn="db://", minconn=1, maxconn=2))

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(r is results[0] for r in results)
    assert calls["count"] == 1
