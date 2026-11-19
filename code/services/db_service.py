"""
Database service for PromptWise using SQLite.
Handles persistent storage for study sessions, prompts, responses, and metrics.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Database path inside code/data/
DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DB_DIR / "history.db"


def get_connection() -> sqlite3.Connection:
    """Create or connect to the SQLite database."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables with appropriate indexes."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                topic TEXT NOT NULL,
                study_mode TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                original_prompt TEXT NOT NULL,
                optimized_prompt TEXT,
                generated_response TEXT NOT NULL,
                metadata_json TEXT
            )
            """
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_topic ON prompt_history(topic)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_mode ON prompt_history(study_mode)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_difficulty ON prompt_history(difficulty)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_timestamp ON prompt_history(timestamp DESC)"
        )
        conn.commit()


def add_history(
    topic: str,
    study_mode: str,
    difficulty: str,
    original_prompt: str,
    optimized_prompt: Optional[str] = None,
    generated_response: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> int:
    """Insert a new study session into history."""
    init_db()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta_str = json.dumps(metadata or {}, ensure_ascii=False)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO prompt_history (
                timestamp, topic, study_mode, difficulty,
                original_prompt, optimized_prompt, generated_response, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                now_str,
                topic.strip(),
                study_mode.strip(),
                difficulty.strip(),
                original_prompt.strip(),
                optimized_prompt.strip() if optimized_prompt else "",
                generated_response.strip(),
                meta_str,
            ),
        )
        conn.commit()
        return cursor.lastrowid or 0


def get_history(
    search_query: str = "",
    mode_filter: Optional[str] = None,
    difficulty_filter: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Retrieve history records with optional search and filters."""
    init_db()
    query = "SELECT * FROM prompt_history WHERE 1=1"
    params: List[Any] = []

    if search_query and search_query.strip():
        term = f"%{search_query.strip()}%"
        query += " AND (topic LIKE ? OR original_prompt LIKE ? OR generated_response LIKE ?)"
        params.extend([term, term, term])

    if mode_filter and mode_filter != "All":
        query += " AND study_mode = ?"
        params.append(mode_filter)

    if difficulty_filter and difficulty_filter != "All":
        query += " AND difficulty = ?"
        params.append(difficulty_filter)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        results = []
        for row in rows:
            item = dict(row)
            try:
                item["metadata"] = json.loads(item.get("metadata_json") or "{}")
            except Exception:
                item["metadata"] = {}
            results.append(item)
        return results


def get_history_by_id(item_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a single history entry by its ID."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prompt_history WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            return None
        item = dict(row)
        try:
            item["metadata"] = json.loads(item.get("metadata_json") or "{}")
        except Exception:
            item["metadata"] = {}
        return item


def delete_history(item_id: int) -> bool:
    """Delete a single history entry by its ID."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prompt_history WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount > 0


def clear_all_history() -> bool:
    """Delete all records from prompt_history."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prompt_history")
        conn.commit()
        return True


def get_history_stats() -> Dict[str, Any]:
    """Get aggregated statistics about saved study sessions."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prompt_history")
        total = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT study_mode, COUNT(*) as cnt 
            FROM prompt_history 
            GROUP BY study_mode 
            ORDER BY cnt DESC
            """
        )
        mode_counts = {row["study_mode"]: row["cnt"] for row in cursor.fetchall()}

        cursor.execute(
            """
            SELECT difficulty, COUNT(*) as cnt 
            FROM prompt_history 
            GROUP BY difficulty
            """
        )
        diff_counts = {row["difficulty"]: row["cnt"] for row in cursor.fetchall()}

        cursor.execute(
            """
            SELECT topic, study_mode, timestamp 
            FROM prompt_history 
            ORDER BY id DESC LIMIT 5
            """
        )
        recent = [dict(row) for row in cursor.fetchall()]

        return {
            "total_sessions": total,
            "mode_counts": mode_counts,
            "difficulty_counts": diff_counts,
            "recent_sessions": recent,
        }
