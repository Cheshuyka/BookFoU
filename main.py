import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea, QGroupBox
from PyQt5.QtWidgets import QLabel, QWidget, QFileDialog, QCheckBox, QDialog
import wikipedia
import warnings
from PyQt5.QtGui import QPixmap
import sqlite3


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

        self.toEditBtn.clicked.connect(self.to_write)
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
            btn = QPushButton('Подробнее')
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
        self.w = ReadWindow()
        self.w.show()

    def to_write(self):  # открытие окна для редактирования файла
        self.write = WriteWindow()
        self.write.show()


class ReadWindow(QWidget):  # окно для открытия книги
    def __init__(self):
        super().__init__()  # TODO: переделать открытие файла
        uic.loadUi('UIs/TEXT.ui', self)
        pass


class AdminOrUser(QDialog):  # выбор админки или юзера
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/AdminOrUser.ui', self)
        self.user_btn.clicked.connect(self.open_user)
        self.admin_btn.clicked.connect(self.open_admin)

    def open_user(self):
        self.w = UserInterface()
        self.w.show()
        self.close()

    def open_admin(self):
        self.w = AdminCheck()
        self.w.show()


class AdminCheck(QDialog):  # проверка на разрешение
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/AdminCheck.ui', self)
        self.check_btn.clicked.connect(self.check)

    def check(self):  # для проверки работы админского интерфейса в логине введите test1, а в пароле 321
        # для проверки работы админского интерфейса со званием super, в логине введите test, а в пароле 123
        login = self.loginEdit.text()
        password = self.passEdit.text()
        con = sqlite3.connect("DBs/Admins_db.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Admins
                    WHERE login = ?""", (login,)).fetchone()
        con.close()
        try:
            assert result
            assert result[1] == password
            print('ok')  # TODO: здесь сделать открытие Admin интерфейса
            self.close()
        except AssertionError:
            self.Error_lbl.setText('Логин или пароль некорректны.\nПовторите попытку')
            self.loginEdit.clear()
            self.passEdit.clear()


class WriteWindow(QWidget):  # окно для редактирования текста
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE.ui', self)
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)

    def to_openFile(self):  # открытие файла
        fname = QFileDialog.getOpenFileName(self, 'Выбрать текст', '')[0]
        writing = open(fname, mode='rt', encoding='utf-8')
        self.textEdit.setPlainText(writing.read())
        writing.close()

    def to_clearFile(self):  # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self):  # сохранение файла
        fname = QFileDialog.getSaveFileName(self, 'Сохраняем', '')[0]
        writing = open(fname, mode='w', encoding='utf-8')
        writing.write(self.textEdit.toPlainText())
        writing.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AdminOrUser()
    ex.show()
    sys.exit(app.exec_())
