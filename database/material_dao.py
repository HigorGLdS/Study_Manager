import sqlite3
from utils.path import get_database_path


class MaterialDAO:
    def __init__(self):
        self.conn = sqlite3.connect(get_database_path())
        self.conn.row_factory = sqlite3.Row

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ==========================
    # FETCH
    # ==========================
    def fetch_all(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    m.id,
                    m.title,
                    m.author,
                    m.type,
                    m.progress,
                    m.category_id,
                    c.name AS category
                FROM materials m
                LEFT JOIN categories c ON c.id = m.category_id
                ORDER BY m.id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    # ==========================
    # INSERT
    # ==========================
    def insert(self, material):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO materials (
                    title, author, type, progress, category_id
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                material["title"],
                material["author"],
                material["type"],
                material["progress"],
                material["category_id"]
            ))
            conn.commit()

    # ==========================
    # UPDATE PROGRESS
    # ==========================
    def update_progress(self, material_id, progress):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE materials
                SET progress = ?
                WHERE id = ?
            """, (progress, material_id))
            conn.commit()