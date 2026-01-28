from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QComboBox, QSpinBox, QPushButton
)


class AddMaterialDialog(QDialog):
    def __init__(self, categories, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Adicionar Material")
        self.setFixedWidth(320)

        layout = QVBoxLayout(self)

        self.title = QLineEdit()
        self.title.setPlaceholderText("Título")

        self.author = QLineEdit()
        self.author.setPlaceholderText("Autor")

        self.type = QComboBox()
        self.type.addItems(["Livro", "Curso", "Artigo", "Vídeo"])

        # 🔑 categoria com ID
        self.category = QComboBox()
        for c in categories:
            self.category.addItem(c["name"], c["id"])

        self.progress = QSpinBox()
        self.progress.setRange(0, 100)
        self.progress.setSuffix(" %")

        btn = QPushButton("Salvar")
        btn.clicked.connect(self.accept)

        for w in (
            self.title, self.author,
            self.type, self.category,
            self.progress, btn
        ):
            layout.addWidget(w)

    def get_data(self):
        return {
            "title": self.title.text().strip(),
            "author": self.author.text().strip(),
            "type": self.type.currentText(),
            "category_id": self.category.currentData(),
            "progress": self.progress.value()
        }