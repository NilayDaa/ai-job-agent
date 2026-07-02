import sqlite3

DB_PATH = "data/jobs.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        link TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()