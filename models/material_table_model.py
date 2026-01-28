from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from datetime import datetime


class MaterialTableModel(QAbstractTableModel):
    HEADERS = ["Título", "Autor", "Tipo", "Categoria", "Progresso"]

    def __init__(self, materials=None):
        super().__init__()
        self._materials = materials or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._materials)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        m = self._materials[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 4:
                return f'{m["progress"]}%'
            return [
                m["title"],
                m["author"],
                m["type"],
                m["category"]
            ][col]

        if role == Qt.EditRole and col == 4:
            return m["progress"]

        if role == Qt.TextAlignmentRole and col == 4:
            return Qt.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]
        return None

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 4:
            flags |= Qt.ItemIsEditable
        return flags

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole and index.column() == 4:
            material = self._materials[index.row()]
            material["progress"] = int(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def add_material(self, material):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._materials.append(material)
        self.endInsertRows()