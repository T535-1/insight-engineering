# core/storage/db.py
from __future__ import annotations
import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).resolve().parents[2] / "data"
DB_PATH = DB_DIR / "insight_engineering.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT,
    balance_index REAL,
    scores_json TEXT
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    facet TEXT,
    priority REAL,
    tips_json TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    type TEXT, -- 'daily' or 'weekly'
    plan_json TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
"""

def get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    with conn:
        conn.executescript(SCHEMA)
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"✅ Database initialized at {DB_PATH}")
