from sentence_transformers import SentenceTransformer
import psycopg2


model = SentenceTransformer('all-MiniLM-L12-v2')


def embed_text(text: str):
    return model.encode(text)


def insert_embedding(conn, text: str, embedding):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO embeddings (chunk_tsv, embedding) VALUES (to_tsvector('english', %s), %s)",
            (text, embedding),
        )
        conn.commit()


def hybrid_search(conn, query: str):
    emb = embed_text(query)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM embeddings
            WHERE chunk_tsv @@ plainto_tsquery(%s)
            ORDER BY embedding <-> %s LIMIT 50;
            """,
            (query, emb),
        )
        return cur.fetchall()


def update_feedback(conn, id: int, boost: float = 0.1):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE embeddings SET feedback_boost = feedback_boost + %s WHERE id = %s",
            (boost, id),
        )
        conn.commit()
