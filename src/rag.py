from __future__ import annotations

import logging
import os
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable

from psycopg2.pool import SimpleConnectionPool
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


# --- Model loading -------------------------------------------------------
_model_lock = threading.Lock()
model: SentenceTransformer | None = None


def init_model() -> SentenceTransformer:
    """Lazily initialize and return the text embedding model."""
    global model
    if model is None:
        with _model_lock:
            if model is None:
                model = SentenceTransformer("all-MiniLM-L12-v2")
    return model


# --- Connection pool -----------------------------------------------------


class ConnectionPool:
    """Wrapper around :class:`SimpleConnectionPool` with context manager access."""

    def __init__(self, dsn: str, minconn: int, maxconn: int) -> None:
        self._pool = SimpleConnectionPool(minconn, maxconn, dsn)

    @contextmanager
    def connection(self):
        conn = self._pool.getconn()
        try:
            yield conn
        finally:
            self._pool.putconn(conn)

    def close(self) -> None:
        self._pool.closeall()


pool: ConnectionPool | None = None


def init_connection_pool(
    dsn: str | None = None, minconn: int = 1, maxconn: int = 10
) -> ConnectionPool:
    """Initialize a connection pool for PostgreSQL."""
    global pool
    if pool is None:
        dsn = dsn or os.getenv("DATABASE_URL")
        if not dsn:
            raise ValueError("DSN required for connection pool")
        pool = ConnectionPool(dsn, minconn, maxconn)
    return pool


def close_pool() -> None:
    """Close the global connection pool if it exists."""
    global pool
    if pool is not None:
        pool.close()
        pool = None


# --- Embedding helpers ---------------------------------------------------


def embed_text(text: str) -> Iterable[float]:
    """Return an embedding vector for the provided text."""
    return init_model().encode(text)


# --- Dataclasses ---------------------------------------------------------


@dataclass
class InsertEmbeddingResult:
    id: int


@dataclass
class HybridSearchResult:
    rows: list


@dataclass
class UpdateFeedbackResult:
    updated: int


# --- Database operations -------------------------------------------------


def insert_embedding(text: str, embedding: Iterable[float]) -> InsertEmbeddingResult:
    """Insert an embedding into the database."""
    if pool is None:
        raise RuntimeError("Connection pool not initialized")
    with pool.connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO embeddings (chunk_tsv, embedding) VALUES (to_tsvector('english', %s), %s) RETURNING id",
                    (text, embedding),
                )
                inserted_id = cur.fetchone()[0]
            conn.commit()
            return InsertEmbeddingResult(id=inserted_id)
        except Exception:  # pragma: no cover - logging
            conn.rollback()
            logger.exception("Failed to insert embedding")
            raise


def hybrid_search(query: str) -> HybridSearchResult:
    """Perform hybrid full-text and vector similarity search."""
    if pool is None:
        raise RuntimeError("Connection pool not initialized")
    emb = embed_text(query)
    with pool.connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT * FROM embeddings
                    WHERE chunk_tsv @@ plainto_tsquery(%s)
                    ORDER BY embedding <-> %s LIMIT 50;
                    """,
                    (query, emb),
                )
                rows = cur.fetchall()
            return HybridSearchResult(rows=rows)
        except Exception:  # pragma: no cover - logging
            conn.rollback()
            logger.exception("Failed to perform hybrid search")
            raise


def update_feedback(id: int, boost: float = 0.1) -> UpdateFeedbackResult:
    """Adjust feedback boost for an embedding row."""
    if pool is None:
        raise RuntimeError("Connection pool not initialized")
    with pool.connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE embeddings SET feedback_boost = feedback_boost + %s WHERE id = %s",
                    (boost, id),
                )
                updated = cur.rowcount
            conn.commit()
            return UpdateFeedbackResult(updated=updated)
        except Exception:  # pragma: no cover - logging
            conn.rollback()
            logger.exception("Failed to update feedback")
            raise
