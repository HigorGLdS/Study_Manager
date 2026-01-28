from PySide6.QtCore import Qt
from models.material_table_model import MaterialTableModel


def test_edit_progress():
    materials = [{
        "title": "Test",
        "author": "Me",
        "type": "Livro",
        "category": "Backend",
        "progress": 20
    }]

    model = MaterialTableModel(materials)
    index = model.index(0, 4)

    assert model.setData(index, 80, Qt.EditRole)
    assert materials[0]["progress"] == 80