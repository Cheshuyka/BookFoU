from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from MyFrameworks.WorkWithFiles import WorkWithFiles
import sqlite3


class WriteEssay():
    def __init__(self):
        self.write = WriteWindow()
        self.read = ReadTask()
        self.write.show()
        self.read.show()


class ReadTask(QWidget):  # окно для вывода задания для сочинения
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/ReadTask.ui', self)
        self.save.clicked.connect(self.to_saveFile)
        self.workerFiles = WorkWithFiles()
        self.getTheme.clicked.connect(self.theme)
        self.tableWidget.verticalHeader().setVisible(True)

    def to_saveFile(self):  # сохранение файла
        self.workerFiles.SaveFiles(self.taskText.toPlainText())

    def theme(self):
        f = open('Essays/LastWritten.txt', mode='rt', encoding='utf-8')
        key = f.read()
        f.close()
        f = open('Essays/LastWritten.txt', mode='w', encoding='utf-8')
        f.write(str(int(key) + 1))
        f.close()
        g = open(f'Essays/Essay {key}.txt', mode='rt', encoding='utf-8')
        s = g.read()
        g1 = open('Essays/Task.txt', mode='rt', encoding='utf-8')
        s1 = g1.read()
        s2 = s1 + '\n\n' + s
        self.taskText.setPlainText(s2)

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
    def __init__(self, text_name, file_name):
        super().__init__()
        uic.loadUi('UIs/TEXT.ui', self)
        self.text_name = text_name
        self.workerFiles = WorkWithFiles()  # экземпляр класса с функционалом для открытия файлов
        self.save_btn.clicked.connect(self.to_save)
        text = open(file_name, mode='rt', encoding='utf-8')  # открытие текста книги
        key = text.read()
        self.textEdit.setPlainText(key)  # помещаем текст книги в поле для текста
        self.setWindowTitle(text_name)
        text.close()
        self.read_btn.clicked.connect(self.set_read)
        con = sqlite3.connect("DBs/Books_db.sqlite")
        check = con.cursor()
        result = check.execute("""SELECT alreadyRead FROM Books
                    WHERE name = ?""", (self.text_name,)).fetchone()
        con.close()
        if result[0]:  # если книга уже прочитана
            self.read_btn.setStyleSheet('background-color: lightgreen; color: white')
            self.read_btn.setText('Прочитано')

    def to_save(self):  # сохранение книги в отдельный файл
        self.workerFiles.SaveFiles(self.textEdit.toPlainText())

    def set_read(self):
        con = sqlite3.connect("DBs/Books_db.sqlite")
        check = con.cursor()
        if self.read_btn.text() == 'Не прочитано':  # если на книге еще нет отметки 'прочитано'
            self.read_btn.setStyleSheet('background-color: lightgreen; color: white')  # изменяем стиль кнопки
            self.read_btn.setText('Прочитано')
            check.execute("""UPDATE Books
                    SET alreadyRead = 1
                    WHERE name = ?""", (self.text_name,))
        else:  # если отметка уже есть
            self.read_btn.setStyleSheet('background-color: white; color: black')
            self.read_btn.setText('Не прочитано')
            check.execute("""UPDATE Books
                    SET alreadyRead = 0
                    WHERE name = ?""", (self.text_name,))
        con.commit()
        con.close()