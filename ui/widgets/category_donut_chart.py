from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QFont, QColor
from PySide6.QtCore import Qt, Signal


class CategoryDonutChart(QWidget):
    categoryClicked = Signal(object)

    def __init__(self):
        super().__init__()

        self.series = QPieSeries()
        self.series.setHoleSize(0.45)

        self.base_font = QFont("Segoe UI", 10)
        self.selected_font = QFont("Segoe UI", 10)
        self.selected_font.setBold(True)

        self.base_color = QColor("#BBBBBB")
        self.selected_color = QColor("#FFFFFF")

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Distribuição por Categoria")
        self.chart.legend().setAlignment(Qt.AlignRight)

        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.series.clicked.connect(self._on_slice_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

    # 🔒 CHAMAR APENAS EM:
    # - init
    # - add/remove material
    def update_chart(self, materials):
        self.series.clear()

        if not materials:
            return

        grouped = {}
        total = len(materials)

        for m in materials:
            cid = m["category_id"]
            cname = m["category"]
            grouped.setdefault(cid, {"name": cname, "count": 0})
            grouped[cid]["count"] += 1

        for cid, data in grouped.items():
            percent = round(data["count"] * 100 / total, 1)
            slice_ = self.series.append(
                f'{data["name"]} ({percent}%)',
                data["count"]
            )
            slice_.setProperty("category_id", cid)
            slice_.setLabelVisible(True)
            slice_.setLabelFont(self.base_font)
            slice_.setLabelColor(self.base_color)

    # 🎯 APENAS VISUAL
    def highlight_category(self, category_id):
        for s in self.series.slices():
            selected = s.property("category_id") == category_id
            s.setExploded(selected)
            s.setLabelFont(self.selected_font if selected else self.base_font)
            s.setLabelColor(self.selected_color if selected else self.base_color)

    def _on_slice_clicked(self, slice_):
        cid = slice_.property("category_id")
        self.highlight_category(cid)
        self.categoryClicked.emit(cid)