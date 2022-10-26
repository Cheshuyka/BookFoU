import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea, QGroupBox
from PyQt5.QtWidgets import QLabel, QWidget, QFileDialog, QCheckBox, QDialog
import wikipedia
import warnings
from PyQt5.QtGui import QPixmap
import sqlite3
from WorkWithFiles import WorkWithFiles


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
            v.addWidget(QLabel(book[0]))
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
        pass


class PasswordCheck(QDialog):  # проверка на разрешение
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/UserCheck.ui', self)
        self.check_btn.clicked.connect(self.check)

    def check(self):  # для проверки работы админского интерфейса в логине введите test1, а в пароле 321
        # для проверки работы админского интерфейса со званием super, в логине введите test, а в пароле 123
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
            self.w = UserInterface()
            self.w.show()
            self.close()
        except AssertionError:
            self.Error_lbl.setText('Логин или пароль некорректны.\nПовторите попытку')
            self.loginEdit.clear()
            self.passEdit.clear()

class ReadWindow(QWidget):  # окно для открытия книги
    def __init__(self, file_name, text_name):
        super().__init__()
        uic.loadUi('UIs/TEXT.ui', self)
        self.save_btn.clicked.connect(self.to_save)
        text = open(file_name, mode='rt', encoding='utf-8')
        key = text.read()
        self.textEdit.setPlainText(key)
        self.setWindowTitle(text_name)
        text.close()

    def to_save(self):
        WorkWithFiles.SaveFiles(self.textEdit.toPlainText())


class WriteWindow(QWidget):  # окно для редактирования текста
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE.ui', self)
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)

    def to_openFile(self):  # открытие файла
        WorkWithFiles.OpenFiles()

    def to_clearFile(self):  # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self):  # сохранение файла
        WorkWithFiles.SaveFiles(self.textEdit.toPlainText())


class Enter(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/Enter.ui', self)
        self.CheckUser.clicked.connect(self.check)
        self.AddUser.clicked.connect(self.add)

    def check(self):
        self.w = PasswordCheck()
        self.w.open()

    def add(self):
        self.w = UserAdd()
        self.w.show()


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
                    WHERE login = ?""", (login,)).fetchone()
        try:
            assert not(result)
        except AssertionError:
            self.Error_lbl.setText('Логин уже используется.\nПовторите попытку')
            return
        cur = con.cursor()
        cur.execute("""INSERT INTO Users(login, password) 
        VALUES(?, ?)""", (login, password)).fetchone()
        con.commit()
        con.close()
        self.w = UserInterface()
        self.w.show()
        self.close()


class WriteEssayWindow(QWidget):  # окно для редактирования текста
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE.ui', self)
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)
        self.getTheme.clicked.connect(self.show_theme)

    def to_openFile(self):  # открытие файла
        WorkWithFiles.OpenFiles()

    def show_theme(self):  # открытие файла
        pass

    def to_clearFile(self):  # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self):  # сохранение файла
        WorkWithFiles.SaveFiles(self.textEdit.toPlainText())


if __name__ == '__main__':
    # con = sqlite3.connect("DBs/Users_db.sqlite")
    # check = con.cursor()
    # result = check.execute("""DELETE FROM Users""").fetchall()
    # print(result)
    app = QApplication(sys.argv)
    ex = Enter()
    ex.show()
    sys.exit(app.exec_())