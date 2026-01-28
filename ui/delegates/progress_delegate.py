from PySide6.QtWidgets import QStyledItemDelegate, QSlider
from PySide6.QtCore import Qt


class ProgressDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        slider = QSlider(Qt.Horizontal, parent)
        slider.setRange(0, 100)
        return slider

    def setEditorData(self, editor, index):
        editor.setValue(index.model().data(index, Qt.EditRole))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), Qt.EditRole)