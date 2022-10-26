from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog


class WorkWithFiles(QWidget):
    def SaveFiles(self, to_write):
        fname = QFileDialog.getSaveFileName(self, 'Сохраняем', '')[0]
        writing = open(fname, mode='w', encoding='utf-8')
        writing.write(to_write)
        writing.close()

    def OpenFiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать текст', '')[0]
        with open(fname, mode='rt', encoding='utf-8') as writing:
            return writing.read()