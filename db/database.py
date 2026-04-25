import sqlite3
from pathlib import Path

DB_PATH = "content.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def _connect(path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path: str = DB_PATH) -> None:
    """Create tables from schema.sql if they don't exist."""
    conn = _connect(path)
    try:
        conn.executescript(SCHEMA_PATH.read_text())
        conn.commit()
    finally:
        conn.close()


def add_clip(
    file_path: str,
    title: str | None = None,
    notes: str | None = None,
    duration_seconds: int | None = None,
    recorded_at: str | None = None,
    path: str = DB_PATH,
) -> dict | None:
    """Register a clip. Returns the inserted row dict, or None if file_path is already registered."""
    conn = _connect(path)
    try:
        cur = conn.execute(
            "INSERT OR IGNORE INTO clips "
            "(file_path, title, notes, duration_seconds, recorded_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (file_path, title, notes, duration_seconds, recorded_at),
        )
        conn.commit()
        if cur.rowcount == 0:
            return None
        row = conn.execute("SELECT * FROM clips WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


# Stubs — each lands with its command in a subsequent commit.

def get_clip(clip_id: int, path: str = DB_PATH) -> dict | None:
    raise NotImplementedError("get_clip lands with `caption draft`")


def add_caption(*args, **kwargs) -> dict:
    raise NotImplementedError("`caption draft` is the next vertical slice")


def add_schedule(*args, **kwargs) -> dict:
    raise NotImplementedError("`schedule` lands after caption draft")


def record_metric(*args, **kwargs) -> dict:
    raise NotImplementedError("`metrics record` lands with the metrics group")


def list_schedules(*args, **kwargs) -> list[dict]:
    raise NotImplementedError("`queue` lands with the schedules group")
