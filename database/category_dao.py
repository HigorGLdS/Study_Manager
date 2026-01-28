import sqlite3
from utils.path import get_database_path


class CategoryDAO:
    def __init__(self):
        self.conn = sqlite3.connect(get_database_path())
        self.conn.row_factory = sqlite3.Row

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def fetch_all(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name
                FROM categories
                ORDER BY name
            """)
            return [dict(row) for row in cursor.fetchall()]

    def insert(self, name):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO categories (name)
                VALUES (?)
            """, (name,))
            conn.commit()