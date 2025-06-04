from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/activities")
def get_logs():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
