from collections import defaultdict
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries,
    QBarSet, QBarCategoryAxis, QValueAxis
)
from PySide6.QtCore import Qt, QEasingCurve
from PySide6.QtGui import QFont, QPainter


class CategoryBarChart(QWidget):
    """
    Gráfico de barras SEMPRE GLOBAL.
    Nunca recebe lista filtrada.
    """

    def __init__(self):
        super().__init__()

        font = QFont("Segoe UI", 11)

        self.chart = QChart()
        self.chart.setTitle("Progresso Médio por Categoria")
        self.chart.setTitleFont(font)
        self.chart.legend().setVisible(False)

        self.series = QBarSeries()
        self.chart.addSeries(self.series)

        self.axis_x = QBarCategoryAxis()
        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, 100)

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setAnimationDuration(600)
        self.chart.setAnimationEasingCurve(QEasingCurve.InOutCubic)

        view = QChartView(self.chart)
        view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout(self)
        layout.addWidget(view)

    def update_chart(self, materials):
        """
        materials = LISTA GLOBAL (sem filtro)
        """
        self.series.clear()
        self.axis_x.clear()

        if not materials:
            return

        grouped = defaultdict(list)

        for m in materials:
            if not m.get("category"):
                continue
            grouped[m["category"]].append(m["progress"])

        bar_set = QBarSet("Progresso Médio")
        categories = []

        for category in sorted(grouped.keys()):
            values = grouped[category]
            avg = sum(values) / len(values)
            bar_set.append(avg)
            categories.append(category)

        self.series.append(bar_set)
        self.axis_x.append(categories)