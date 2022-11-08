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

    def OpenFiles(self, type='Текст', to_return='Текст'):  # открытие файла
        try:
            if type == 'Текст':
                fname = QFileDialog.getOpenFileName(self, 'Выбрать текст', '')[0]
                if to_return == 'Текст':
                    with open(fname, mode='rt', encoding='utf-8') as writing:
                        return writing.read()
                elif to_return == 'Имя':
                    return fname
            elif type == 'Картинка':
                fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
                return fname
        except FileNotFoundError:
            pass