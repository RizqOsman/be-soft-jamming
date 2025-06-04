import sqlite3

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

conn.commit()
conn.close()

print("✅ Tabel 'logs' berhasil dibuat di logs.db")
