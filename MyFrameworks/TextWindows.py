from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from MyFrameworks.WorkWithFiles import WorkWithFiles
from random import choice


class WriteEssayWindow(QWidget):  # окно для редактирования сочинений
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE_ESSAY.ui', self)
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)
        self.getTheme.clicked.connect(self.show_theme)
        self.workerFiles = WorkWithFiles()

    def to_openFile(self):  # открытие файла
        self.textEdit.setPlainText(self.workerFiles.OpenFiles())

    def show_theme(self):  # получение темы для сочинения
        f = open("DBs/Essays.txt", mode="rt", encoding='utf-8')
        key = list(map(lambda x: x.strip('\n'), f.readlines()))
        theme = choice(key)
        self.theme_lbl.setText(theme)

    def to_clearFile(self):  # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self):  # сохранение файла
        self.textEdit.setPlainText(self.workerFiles.SaveFiles(self.textEdit.toPlainText()))


class WriteWindow(QWidget):  # окно для редактирования заметок
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE.ui', self)
        self.workerFiles = WorkWithFiles()
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)

    def to_openFile(self):  # открытие файла
        self.textEdit.setPlainText(self.workerFiles.OpenFiles())

    def to_clearFile(self):  # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self):  # сохранение файла
        self.workerFiles.SaveFiles(self.textEdit.toPlainText())


class ReadWindow(QWidget):  # окно для открытия книги
    def __init__(self, file_name, text_name):
        super().__init__()
        uic.loadUi('UIs/TEXT.ui', self)
        self.file_name = file_name  # название файла с книгой
        self.workerFiles = WorkWithFiles()  # экземпляр класса с функционалом для открытия файлов
        self.save_btn.clicked.connect(self.to_save)
        text = open(self.file_name, mode='rt', encoding='utf-8')  # открытие текста книги
        key = text.read()
        self.textEdit.setPlainText(key)  # помещаем текст книги в поле для текста
        self.setWindowTitle(text_name)
        text.close()
        self.read_btn.clicked.connect(self.set_read)
        f = open('DBs/alreadyRead.txt', mode='r+', encoding='utf-8')  # открываем файл с названиями прочитанных книг
        self.key1 = list(map(lambda x: x.strip('\n'), f.readlines()))
        f.close()

        if self.file_name in self.key1:  # если книга уже прочитана
            self.read_btn.setStyleSheet('background-color: lightgreen; color: white')
            self.read_btn.setText('Прочитано')

    def to_save(self):  # сохранение книги в отдельный файл
        self.workerFiles.SaveFiles(self.textEdit.toPlainText())

    def set_read(self):
        f = open('DBs/alreadyRead.txt', mode='r+', encoding='utf-8')  # открытие файла со списком прочитанных книг
        if self.read_btn.text() == 'Не прочитано':  # если на книге еще нет отметки 'прочитано'
            self.read_btn.setStyleSheet('background-color: lightgreen; color: white')  # изменяем стиль кнопки
            self.read_btn.setText('Прочитано')
            self.key1.append(self.file_name)  # добавление книги в список прочитанных
            f.truncate(0)
            f.write('\n'.join(self.key1))
        else:  # если отметка уже есть
            self.read_btn.setStyleSheet('background-color: white; color: black')
            self.read_btn.setText('Не прочитано')
            self.key1.remove(self.file_name)  # удаление книги из списка прочитанных
            f.truncate(0)
            f.write('\n'.join(self.key1))
        f.close()