from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog


class WorkWithFiles(QWidget):
    def SaveFiles(self, write):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Сохраняем', '')[0]
            writing = open(fname, mode='w', encoding='utf-8')
            writing.write(write)
            writing.close()
        except FileNotFoundError:
            pass

    def OpenFiles(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать текст', '')[0]
            with open(fname, mode='rt', encoding='utf-8') as writing:
                return writing.read()
        except FileNotFoundError:
            pass