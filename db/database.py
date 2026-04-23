import sqlite3
from pathlib import Path

DB_PATH = "content.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def _connect(path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path: str = DB_PATH) -> None:
    """Create tables from schema.sql if they don't exist."""
    conn = _connect(path)
    try:
        conn.executescript(SCHEMA_PATH.read_text())
        conn.commit()
    finally:
        conn.close()


def insert_post(post: dict, path: str = DB_PATH) -> bool:
    """Insert a post into raw_posts. Returns True if new, False if duplicate."""
    cols = ["source", "external_id", "title", "description", "url", "author",
            "likes", "comments", "views", "shares"]
    values = [post.get(c) for c in cols]
    placeholders = ", ".join("?" * len(cols))
    col_list = ", ".join(cols)
    conn = _connect(path)
    try:
        cur = conn.execute(
            f"INSERT OR IGNORE INTO raw_posts ({col_list}) VALUES ({placeholders})",
            values,
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def get_posts(source: str | None = None, limit: int = 50, path: str = DB_PATH) -> list[dict]:
    """Return posts from raw_posts ordered by likes DESC, optionally filtered by source."""
    conn = _connect(path)
    try:
        if source:
            rows = conn.execute(
                "SELECT * FROM raw_posts WHERE source = ? ORDER BY likes DESC LIMIT ?",
                (source, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM raw_posts ORDER BY likes DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
