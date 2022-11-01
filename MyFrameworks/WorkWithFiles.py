from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog


class WorkWithFiles(QWidget):  # класс для работы с файлами
    def SaveFiles(self, write):  # сохранение файла
        try:
            fname = QFileDialog.getSaveFileName(self, 'Сохраняем', '')[0]
            writing = open(fname, mode='w', encoding='utf-8')
            writing.write(write)
            writing.close()
        except FileNotFoundError:
            pass

    def OpenFiles(self):  # открытие файла
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать текст', '')[0]
            with open(fname, mode='rt', encoding='utf-8') as writing:
                return writing.read()
        except FileNotFoundError:
            pass