import sqlite3
from datetime import datetime

def log_event(action: str, interface: str, target: str):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            interface TEXT,
            target TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO logs (timestamp, action, interface, target) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(), action, interface, target)
    )

    conn.commit()
    conn.close()
