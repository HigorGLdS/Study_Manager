from PySide6.QtWidgets import QInputDialog


def get_new_category(parent=None):
    name, ok = QInputDialog.getText(
        parent,
        "Nova Categoria",
        "Nome da categoria:"
    )
    return name.strip() if ok and name.strip() else None