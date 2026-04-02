import sqlite3
from datetime import datetime

DB = "vagas.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS applied (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            applied_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def mark_applied(job):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        INSERT OR IGNORE INTO applied VALUES (?, ?, ?, ?)
    """, (
        job["id"],
        job["title"],
        job["company"],
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_applied():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT id, title, company, applied_at FROM applied")
    rows = c.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "company": r[2],
            "applied_at": r[3]
        }
        for r in rows
    ]