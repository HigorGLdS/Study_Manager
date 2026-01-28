import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "study.db"


class CategoryDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name
            FROM categories
            ORDER BY name
        """)
        return [dict(row) for row in cursor.fetchall()]

    def insert(self, name):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO categories (name)
            VALUES (?)
        """, (name,))
        self.conn.commit()
