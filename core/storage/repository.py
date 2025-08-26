# core/storage/repository.py
from __future__ import annotations
import json
from typing import Dict, List, Any, Optional
from .db import get_connection

def save_session(user_id: str, balance_index: float, scores: Dict[str, float]) -> int:
    conn = get_connection()
    with conn:
        cur = conn.execute(
            "INSERT INTO sessions (user_id, balance_index, scores_json) VALUES (?, ?, ?)",
            (user_id, balance_index, json.dumps(scores, ensure_ascii=False)),
        )
        return cur.lastrowid

def save_recommendations(session_id: int, recs: List[Dict[str, Any]]) -> None:
    conn = get_connection()
    with conn:
        for r in recs:
            conn.execute(
                "INSERT INTO recommendations (session_id, facet, priority, tips_json) VALUES (?, ?, ?, ?)",
                (
                    session_id,
                    r["facet"],
                    r["priority"],
                    json.dumps(r["tips"], ensure_ascii=False),
                ),
            )

def save_plan(session_id: int, plan_type: str, plan: Dict[str, Any]) -> None:
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO plans (session_id, type, plan_json) VALUES (?, ?, ?)",
            (session_id, plan_type, json.dumps(plan, ensure_ascii=False)),
        )

def list_sessions(limit: int = 10) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.execute(
        "SELECT id, created_at, user_id, balance_index, scores_json FROM sessions ORDER BY created_at DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    return [
        {
            "id": r[0],
            "created_at": r[1],
            "user_id": r[2],
            "balance_index": r[3],
            "scores": json.loads(r[4] or "{}"),
        }
        for r in rows
    ]

def get_session(session_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.execute(
        "SELECT id, created_at, user_id, balance_index, scores_json FROM sessions WHERE id=?",
        (session_id,),
    )
    row = cur.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "created_at": row[1],
        "user_id": row[2],
        "balance_index": row[3],
        "scores": json.loads(row[4] or "{}"),
    }

def get_recommendations(session_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.execute(
        "SELECT facet, priority, tips_json FROM recommendations WHERE session_id=?",
        (session_id,),
    )
    return [
        {"facet": r[0], "priority": r[1], "tips": json.loads(r[2] or "[]")}
        for r in cur.fetchall()
    ]

def get_plan(session_id: int, plan_type: str = "daily") -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.execute(
        "SELECT plan_json FROM plans WHERE session_id=? AND type=?",
        (session_id, plan_type),
    )
    row = cur.fetchone()
    return json.loads(row[0]) if row else None

def delete_session(session_id: int):
    conn = get_connection()
    with conn:
        conn.execute("DELETE FROM sessions WHERE id=?", (session_id,))
