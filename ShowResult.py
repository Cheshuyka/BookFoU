from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class Result(QMainWindow):
    def __init__(self, correct, incorrect, skipped):
        super().__init__()
        self.setWindowTitle("Result")
        self.setGeometry(200, 200, 700, 700)

        series = QPieSeries()
        series.append("Правильно", correct)
        series.append("Неправильно", incorrect)
        series.append("Пропущено", skipped)
        slice = QPieSlice()
        slice = series.slices()[0]
        slice.setExploded(True)
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeBrownSand)
        chart.setTitle("Результат теста")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(chartview)