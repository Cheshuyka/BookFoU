from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtChart import QChart, QChartView, QPieSeries


class Result(QMainWindow):  # класс для вывода диаграммы (результат теста)
    def __init__(self, correct, incorrect, skipped, file, name):
        super().__init__()
        self.setWindowTitle("Результат")
        self.setGeometry(200, 200, 700, 700)

        series = QPieSeries()
        series.append(f"Правильно ({correct})", correct)
        series.append(f"Неправильно ({incorrect})", incorrect)
        series.append(f"Пропущено ({skipped})", skipped)
        part = series.slices()[0]  # выделенный кусок в круговой диаграмме
        part.setExploded(True)  # выделяем кусок
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)  # анимация диаграммы
        chart.setTheme(QChart.ChartThemeBrownSand)  # тема диаграммы
        chart.setTitle("Результат теста")
        chartview = QChartView(chart)
        self.setCentralWidget(chartview)
        f = open(file, mode='rt', encoding='utf-8')
        results = list(map(lambda x: x.strip('\n'), f))
        res = list(filter(lambda x: name in x, results))
        f.close()
        f = open(file, mode='w', encoding='utf-8')
        a = round(correct / (incorrect + skipped + correct) * 100, 2)
        if res:
            res = res[0]
            if float(res.split(':')[1].strip('%')) < a:
                results.remove(res)
                results.append(f'{name}:{a}%')
                f.write('\n'.join(results))
            else:
                f.write('\n'.join(results))
        else:
            results.append(f'{name}:{a}%')
            f.write('\n'.join(results))
        f.close()