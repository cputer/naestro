from sentence_transformers import SentenceTransformer
from psycopg2.pool import SimpleConnectionPool
import logging
import os


model = SentenceTransformer("all-MiniLM-L12-v2")

logger = logging.getLogger(__name__)

pool: SimpleConnectionPool | None = None


def init_connection_pool(
    dsn: str | None = None, minconn: int = 1, maxconn: int = 10
) -> SimpleConnectionPool:
    """Initialize a connection pool for PostgreSQL."""
    global pool
    if pool is None:
        dsn = dsn or os.getenv("DATABASE_URL")
        if not dsn:
            raise ValueError("DSN required for connection pool")
        pool = SimpleConnectionPool(minconn, maxconn, dsn)
    return pool


def _get_conn():
    if pool is None:
        raise RuntimeError("Connection pool not initialized")
    return pool.getconn()


def _put_conn(conn):
    if pool:
        pool.putconn(conn)


def embed_text(text: str):
    return model.encode(text)


def insert_embedding(text: str, embedding):
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO embeddings (chunk_tsv, embedding) VALUES (to_tsvector('english', %s), %s) RETURNING id",
                (text, embedding),
            )
            conn.commit()
            inserted_id = cur.fetchone()[0]
        return {"success": True, "id": inserted_id}
    except Exception as exc:
        conn.rollback()
        logger.exception("Failed to insert embedding")
        return {"success": False, "error": str(exc)}
    finally:
        _put_conn(conn)


def hybrid_search(query: str):
    conn = _get_conn()
    emb = embed_text(query)
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
        return {"success": True, "rows": rows}
    except Exception as exc:
        conn.rollback()
        logger.exception("Failed to perform hybrid search")
        return {"success": False, "error": str(exc)}
    finally:
        _put_conn(conn)


def update_feedback(id: int, boost: float = 0.1):
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE embeddings SET feedback_boost = feedback_boost + %s WHERE id = %s",
                (boost, id),
            )
            conn.commit()
            updated = cur.rowcount
        return {"success": True, "updated": updated}
    except Exception as exc:
        conn.rollback()
        logger.exception("Failed to update feedback")
        return {"success": False, "error": str(exc)}
    finally:
        _put_conn(conn)
