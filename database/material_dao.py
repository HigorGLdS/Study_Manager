import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "study.db"


class MaterialDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    # ==========================
    # FETCH
    # ==========================
    def fetch_all(self):
        cursor = self.conn.cursor()
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

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # ==========================
    # INSERT
    # ==========================
    def insert(self, material):
        cursor = self.conn.cursor()
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
        self.conn.commit()

    # ==========================
    # UPDATE PROGRESS
    # ==========================
    def update_progress(self, material_id, progress):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE materials
            SET progress = ?
            WHERE id = ?
        """, (progress, material_id))
        self.conn.commit()