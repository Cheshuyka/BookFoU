import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QGroupBox
from PyQt5.QtWidgets import QLabel, QWidget, QDialog
import wikipedia
import warnings
from PyQt5.QtGui import QPixmap
import sqlite3
from WorkWithFiles import WorkWithFiles
from random import choice

warnings.catch_warnings()
warnings.simplefilter("ignore")


class UserInterface(QMainWindow):  # интерфейс пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/User.ui', self)
        self.wikiGet.clicked.connect(self.wiki)
        wikipedia.set_lang('ru')

        self.group = QGroupBox()
        self.h = QVBoxLayout()
        self.group.setLayout(self.h)
        self.scrollArea.setWidget(self.group)

        self.toWriteNotes.clicked.connect(self.note)
        self.toWriteEssay.clicked.connect(self.essay)
        self.find_btn.clicked.connect(self.findBooks)

        self.findBooks()

    def findBooks(self):
        name = self.nameEdit.text()
        author = self.authorEdit.text()
        if name and author:
            wheres = f"WHERE name LIKE '%{name}%' AND author LIKE '%{author}%'"
        elif name:
            wheres = f"WHERE name LIKE '%{name}%'"
        elif author:
            wheres = f"WHERE author LIKE '%{author}%'"
        else:
            wheres = ''
        con = sqlite3.connect("DBs/Books_db.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM Books
                    {wheres}""").fetchall()
        con.close()
        for i in reversed(range(self.h.count())):
            self.h.itemAt(i).widget().setParent(None)
        for book in result:
            group1 = QGroupBox()
            label = QLabel()
            im = QPixmap(book[3])
            label.setPixmap(im)
            v = QVBoxLayout()
            v.addWidget(label)
            name = QLabel(book[0])
            with open('DBs/alreadyRead.txt', mode='rt', encoding='utf-8') as f:
                key = list(map(lambda x: x.strip('\n'), f.readlines()))
                if book[2] in key:
                    name.setStyleSheet('color: darkgreen')
            v.addWidget(name)
            v.addWidget(QLabel(book[1]))
            btn = QPushButton('Читать')
            btn.setObjectName(book[4])
            btn.clicked.connect(self.to_openBook)
            v.addWidget(btn)
            group1.setLayout(v)
            self.h.addWidget(group1)

    def wiki(self):  # вывод определения слова
        try:
            word = self.wikiLine.text()  # получение слова
            self.wikiText.setText(str(wikipedia.summary(word).split('\n')[0]))  # вывод определения
        except Exception:  # если слово не найдено или поле пусто
            self.wikiText.setText('определение слова не найдено')

    def to_openBook(self):  # открытие книги в отдельном окне
        con = sqlite3.connect("DBs/Books_db.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM Books
                    WHERE btnName = '{self.sender().objectName()}'""").fetchone()
        con.close()
        self.w = ReadWindow(result[2], result[0])
        self.w.show()

    def note(self):  # открытие окна для редактирования файла
        self.write = WriteWindow()
        self.write.show()

    def essay(self):
        self.w = WriteEssayWindow()
        self.w.show()


class PasswordCheck(QDialog):  # проверка на разрешение
    def __init__(self, login):
        super().__init__()
        uic.loadUi('UIs/UserCheck.ui', self)
        self.check_btn.clicked.connect(self.check)
        self.loginEdit.setText(login)
        self.delete_btn.clicked.connect(self.check)

    def check(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()
        con = sqlite3.connect("DBs/Users_db.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Users
                    WHERE login = ?""", (login,)).fetchone()
        con.close()
        try:
            assert result
            assert result[1] == password
            if self.sender().text() == 'удалить пользователя':
                con = sqlite3.connect("DBs/Users_db.sqlite")
                cur = con.cursor()
                result = cur.execute("""DELETE FROM Users
                WHERE login = ?""", (login,))
                con.commit()
                con.close()
                self.w = Enter()
                self.w.show()
                self.close()
            else:
                self.w = UserInterface()
                self.w.show()
                self.close()
        except AssertionError:
            self.Error_lbl.setText('Логин или пароль некорректны.\nПовторите попытку')
            self.loginEdit.clear()


class ReadWindow(QWidget):  # окно для открытия книги
    def __init__(self, file_name, text_name):
        super().__init__()
        uic.loadUi('UIs/TEXT.ui', self)
        self.file_name = file_name
        self.workerFiles = WorkWithFiles()
        self.save_btn.clicked.connect(self.to_save)
        text = open(self.file_name, mode='rt', encoding='utf-8')
        key = text.read()
        self.textEdit.setPlainText(key)
        self.setWindowTitle(text_name)
        text.close()
        self.read_btn.clicked.connect(self.set_read)
        f = open('DBs/alreadyRead.txt', mode='r+', encoding='utf-8')
        self.key1 = list(map(lambda x: x.strip('\n'), f.readlines()))
        f.close()

        if self.file_name in self.key1:
            self.read_btn.setStyleSheet('background-color: lightgreen; color: white')
            self.read_btn.setText('Прочитано')

    def to_save(self):
        self.workerFiles.SaveFiles(self.textEdit.toPlainText())

    def set_read(self):
        f = open('DBs/alreadyRead.txt', mode='r+', encoding='utf-8')
        if self.read_btn.text() == 'Не прочитано':
            self.read_btn.setStyleSheet('background-color: lightgreen; color: white')
            self.read_btn.setText('Прочитано')
            self.key1.append(self.file_name)
            f.truncate(0)
            f.write('\n'.join(self.key1))
        else:
            self.read_btn.setStyleSheet('background-color: white; color: black')
            self.read_btn.setText('Не прочитано')
            self.key1.remove(self.file_name)
            f.truncate(0)
            f.write('\n'.join(self.key1))
        f.close()


class WriteWindow(QWidget):  # окно для редактирования текста
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


class Enter(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/Enter.ui', self)
        self.AddUser.clicked.connect(self.add)

        self.groupBox = QGroupBox()
        self.h = QVBoxLayout()
        self.groupBox.setLayout(self.h)
        self.scrollArea.setWidget(self.groupBox)

        con = sqlite3.connect("DBs/Users_db.sqlite")
        check = con.cursor()
        result = check.execute("""SELECT login FROM Users""").fetchall()
        for i in result:
            btn = QPushButton(i[0])
            btn.clicked.connect(self.check)
            self.h.addWidget(btn)

    def check(self):
        self.w = PasswordCheck(self.sender().text())
        self.w.open()
        self.close()

    def add(self):
        self.w = UserAdd()
        self.w.show()
        self.close()


class UserAdd(QDialog):  # добавление пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/UserAdd.ui', self)
        self.check_btn.clicked.connect(self.add)

    def add(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()
        repeat = self.passRepeat.text()
        try:
            assert password == repeat
            if not(password):
                raise ValueError
        except AssertionError:
            self.Error_lbl.setText('Пароли различны.\nПовторите попытку')
            return
        except ValueError:
            self.Error_lbl.setText('Пароли пустой.\nПовторите попытку')
            return
        con = sqlite3.connect("DBs/Users_db.sqlite")
        check = con.cursor()
        result = check.execute("""SELECT * FROM Users
                    WHERE login = ?""", (login,)).fetchall()
        try:
            assert not(result)
        except AssertionError:
            self.Error_lbl.setText('Логин уже используется.\nПовторите попытку')
            return
        cur = con.cursor()
        cur.execute("""INSERT INTO Users(login, password) 
        VALUES(?, ?)""", (login, password))
        con.commit()
        con.close()
        self.w = UserInterface()
        self.w.show()
        self.close()


class WriteEssayWindow(QWidget):  # окно для редактирования текста
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE_ESSAY.ui', self)
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)
        self.getTheme.clicked.connect(self.show_theme)
        self.openingRecent.clicked.connect(self.show_essays)
        self.workerFiles = WorkWithFiles()

    def to_openFile(self):  # открытие файла
        self.textEdit.setPlainText(self.workerFiles.OpenFiles())

    def show_theme(self):  # открытие файла
        f = open("texts/essays.txt", mode="rt", encoding='utf-8')
        key = list(map(lambda x: x.strip('\n'), f.readlines()))
        theme = choice(key)
        self.theme_lbl.setText(theme)

    def to_clearFile(self):  # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self):  # сохранение файла
        self.textEdit.setPlainText(self.workerFiles.SaveFiles(self.textEdit.toPlainText()))

    def show_essays(self): # TODO: сделать вывод уже написанных сочинений
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Enter()
    ex.show()
    sys.exit(app.exec_())
