from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PySide6.QtCore import Qt
from ui.widgets.category_bar_chart import CategoryBarChart


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        cards = QHBoxLayout()

        self.avg_label = self._card("Progresso Médio", "0%")
        self.done_label = self._card("Concluídos", "0%")

        cards.addWidget(self.avg_label)
        cards.addWidget(self.done_label)

        self.category_chart = CategoryBarChart()

        layout.addLayout(cards)
        layout.addWidget(self.category_chart)

    def _card(self, title, value):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        label = QLabel(f"<b>{title}</b><br>{value}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        frame.label = label
        return frame

    def update_stats(self, materials):
        if not materials:
            self.avg_label.label.setText("<b>Progresso Médio</b><br>0%")
            self.done_label.label.setText("<b>Concluídos</b><br>0%")
            return

        total = len(materials)
        avg = sum(m["progress"] for m in materials) // total
        done = sum(1 for m in materials if m["progress"] == 100)

        self.avg_label.label.setText(f"<b>Progresso Médio</b><br>{avg}%")
        self.done_label.label.setText(
            f"<b>Concluídos</b><br>{int(done / total * 100)}%"
        )