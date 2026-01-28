from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt


class CategoryListWidget(QListWidget):
    def __init__(self, categories):
        super().__init__()
        self.setSelectionMode(QListWidget.SingleSelection)
        self.reload(categories)

    def reload(self, categories):
        self.blockSignals(True)
        self.clear()
        for c in categories:
            item = QListWidgetItem(c["name"])
            item.setData(Qt.UserRole, c["id"])
            self.addItem(item)
        self.blockSignals(False)

    def sync_selection(self, category_id):
        self.blockSignals(True)

        if category_id is None:
            self.clearSelection()
        else:
            for i in range(self.count()):
                item = self.item(i)
                if item.data(Qt.UserRole) == category_id:
                    self.setCurrentItem(item)
                    item.setSelected(True)
                    break

        self.blockSignals(False)