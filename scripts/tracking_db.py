"""
Phase 3: SQLite session/outcome tracking. An append-only log of study/quiz
attempts -- current status for an item is derived by querying the most recent
row, not maintained as a separate table (see LEARNING_LOG.md for why).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path("data/tracking.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS study_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_area TEXT NOT NULL,
    question_number INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Studied', 'Solved', 'Struggled')),
    timestamp TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def init_db(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def log_attempt(conn: sqlite3.Connection, topic_area: str, question_number: int, status: str) -> None:
    conn.execute(
        "INSERT INTO study_log (topic_area, question_number, status) VALUES (?, ?, ?)",
        (topic_area, question_number, status),
    )
    conn.commit()


def get_current_status(conn: sqlite3.Connection, topic_area: str, question_number: int) -> str | None:
    cursor = conn.execute(
        """
        SELECT status FROM study_log
        WHERE topic_area = ? AND question_number = ?
        ORDER BY timestamp DESC, id DESC
        LIMIT 1
        """,
        (topic_area, question_number),
    )
    row = cursor.fetchone()
    return row[0] if row else None  # None means "Not Studied" -- no log rows exist yet
