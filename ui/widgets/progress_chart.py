from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtCore import Qt, QEasingCurve
from PySide6.QtGui import QFont

font = QFont("Segoe UI", 12)


class ProgressChart(QWidget):
    def __init__(self):
        super().__init__()

        self.series = QPieSeries()
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitleFont(font)
        self.chart.setTitle("Distribuição do Progresso")
        self.chart.legend().setFont(font)
        self.chart.legend().setAlignment(Qt.AlignRight)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(self.chart_view.renderHints())

        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart.setAnimationDuration(600)
        self.chart.setAnimationEasingCurve(QEasingCurve.InOutCubic)

        layout = QVBoxLayout(self)
        layout.addWidget(self.chart_view)

    def update_chart(self, materials):
        self.series.clear()

        if not materials:
            return

        done = sum(1 for m in materials if m["progress"] == 100)
        not_started = sum(1 for m in materials if m["progress"] == 0)
        in_progress = len(materials) - done - not_started

        if done:
            self.series.append("Concluídos", done)
        if in_progress:
            self.series.append("Em andamento", in_progress)
        if not_started:
            self.series.append("Não iniciados", not_started)

        # Destacar concluídos
        for slice_ in self.series.slices():
            if slice_.label().startswith("Concluídos"):
                slice_.setExploded(True)
                slice_.setLabelVisible(True)
