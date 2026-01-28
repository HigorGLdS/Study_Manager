import sys
import os
import shutil
from pathlib import Path


def resource_path(relative_path: str) -> Path:
    """
    Retorna o caminho correto para recursos,
    funcionando tanto em desenvolvimento quanto em .exe (PyInstaller)
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent.parent / relative_path


def get_appdata_dir() -> Path:
    base = Path(os.getenv("APPDATA"))
    app_dir = base / "StudyManager"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_database_path() -> Path:
    appdata_db = get_appdata_dir() / "study.db"

    if not appdata_db.exists():
        bundled_db = resource_path("study.db")
        shutil.copy(bundled_db, appdata_db)

    return appdata_db