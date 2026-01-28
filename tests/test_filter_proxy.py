from models.material_filter_proxy import MaterialFilterProxy
from models.material_table_model import MaterialTableModel

def test_filter_by_category(qtbot):
    materials = [
        {"title": "A", "category_id": 1, "category": "Backend", "progress": 10},
        {"title": "B", "category_id": 2, "category": "Frontend", "progress": 20},
    ]

    model = MaterialTableModel(materials)
    proxy = MaterialFilterProxy()
    proxy.setSourceModel(model)

    proxy.set_category(1)
    assert proxy.rowCount() == 1