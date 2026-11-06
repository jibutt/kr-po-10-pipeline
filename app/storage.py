"""Хранение обращений в SQLite. Все запросы параметризованы."""
import sqlite3


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str) -> None:
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner TEXT NOT NULL,
                text TEXT NOT NULL
            )
            """
        )
    conn.close()


def create_ticket(db_path: str, owner: str, text: str) -> int:
    conn = _connect(db_path)
    with conn:
        cur = conn.execute(
            "INSERT INTO tickets (owner, text) VALUES (?, ?)",
            (owner, text),
        )
    conn.close()
    return int(cur.lastrowid)


def get_ticket(db_path: str, ticket_id: int, user: str) -> dict | None:
    """Возвращает обращение только его владельцу; для чужих возвращает None."""
    conn = _connect(db_path)
    row = conn.execute(
        "SELECT id, owner, text FROM tickets WHERE id = ? AND owner = ?",
        (ticket_id, user),
    ).fetchone()
    conn.close()
    return dict(row) if row else None
