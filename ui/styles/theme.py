from pathlib import Path


def load_theme(app, theme_name):
    path = Path(__file__).parent / f"{theme_name}.qss"
    with open(path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
