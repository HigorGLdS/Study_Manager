import sys
import sqlite3
import pytest
from pathlib import Path

# =========================
# PATH DO PROJETO
# =========================
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# =========================
# DB DE TESTE
# =========================
TEST_DB = Path(__file__).parent / "test.db"

@pytest.fixture
def db():
    conn = sqlite3.connect(TEST_DB)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS materials;
        DROP TABLE IF EXISTS categories;

        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );

        CREATE TABLE materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            type TEXT,
            progress INTEGER,
            category_id INTEGER NOT NULL,
            updated_at TEXT,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        );
    """)

    conn.commit()
    yield conn
    conn.close()