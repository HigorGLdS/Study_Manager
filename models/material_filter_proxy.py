from PySide6.QtCore import QSortFilterProxyModel


class MaterialFilterProxy(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._category_id = None
        self._search_text = ""

    def set_category(self, category_id):
        self._category_id = category_id
        self.invalidateFilter()

    def set_search_text(self, text):
        self._search_text = text.lower()
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        model = self.sourceModel()
        material = model._materials[row]

        if self._category_id is not None:
            if material["category_id"] != self._category_id:
                return False

        if self._search_text:
            if self._search_text not in material["title"].lower():
                return False

        return True

    def get_filtered_materials(self):
        model = self.sourceModel()
        result = []

        for row in range(self.rowCount()):
            index = self.index(row, 0)
            source = self.mapToSource(index)
            if source.isValid():
                result.append(model._materials[source.row()])

        return result