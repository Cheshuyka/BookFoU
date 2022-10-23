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


class UserInterface(QMainWindow): # интерфейс пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/User.ui', self)
        self.wikiGet.clicked.connect(self.wiki)
        wikipedia.set_lang('ru')
        #label = QLabel()
        #label1 = QLabel()
        #label2 = QLabel()
        #im = QPixmap(y['спать хочется'])
        #im1 = QPixmap(y['идиот'])
        #im2 = QPixmap(y['преступление и наказание'])
        #label.setPixmap(im)
        #label1.setPixmap(im1)
        #label2.setPixmap(im2)
        self.scroll = QScrollArea()

        self.group = QGroupBox()
        self.group1 = QGroupBox()
        self.filter = QGroupBox()

        self.h = QVBoxLayout()

        self.h.addWidget(self.group1)

        self.group.setLayout(self.h)
        self.scroll.setWidget(self.group)
        self.horizontalLayout.addWidget(self.scroll)
        # self.v = QVBoxLayout()
        # self.v1 = QVBoxLayout()
        # self.v2 = QVBoxLayout()
        # self.v.addWidget(label)
        # self.v.addWidget(QLabel('Спать Хочется'))
        # self.v.addWidget(QLabel('А.П.Чехов'))
        # btn = QPushButton('Подробнее')
        # btn.clicked.connect(self.to_open)
        # self.v.addWidget(btn)
        # self.v1.addWidget(label1)
        # self.v2.addWidget(label2)
        # self.group1.setLayout(self.v)
        # self.group2.setLayout(self.v1)
        # self.group3.setLayout(self.v2)

        #self.group1.setLayout(self.v)
        #self.group2.setLayout(self.v1)

        self.toEditBtn.clicked.connect(self.to_write)

    def wiki(self): # вывод определения слова
        try:
            word = self.wikiLine.text() # получение слова
            self.wikiText.setText(str(wikipedia.summary(word).split('\n')[0])) # вывод определения
        except Exception: # если слово не найдено или поле пусто
            self.wikiText.setText('определение слова не найдено')

    def to_openBook(self): # открытие книги в отдельном окне
        self.w = ReadWindow()
        self.w.show()

    def to_write(self): # открытие окна для редактирования файла
        self.write = WriteWindow()
        self.write.show()

    def show_books(self): # вывод книг в соответствии с выбранными фильтрами
        pass


class ReadWindow(QWidget): # окно для открытия книги
    def __init__(self):
        super().__init__() # TODO: переделать открытие файла
        uic.loadUi('UIs/TEXT.ui', self)
        pass


class AdminOrUser(QDialog): # выбор админки или юзера
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


class AdminCheck(QDialog): # проверка на разрешение
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/AdminCheck.ui', self)
        self.check_btn.clicked.connect(self.check)

    def check(self): # для проверки работы админского интерфейса в логине введите test1, а в пароле 321
        # для проверки работы админского интерфейса со званием super, в логине введите test, а в пароле 123
        login = self.loginEdit.text()
        password = self.passEdit.text()
        con = sqlite3.connect("DBs/Admins_db.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Admins
                    WHERE login = ?""", (login,)).fetchone()
        try:
            assert result
            assert result[1] == password
            print('ok') # TODO: здесь сделать открытие Admin интерфейса
            self.close()
        except AssertionError:
            self.Error_lbl.setText('Логин или пароль некорректны.\nПовторите попытку')
            self.loginEdit.clear()
            self.passEdit.clear()


class WriteWindow(QWidget): # окно для редактирования текста
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE.ui', self)
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)

    def to_openFile(self): # открытие файла
        fname = QFileDialog.getOpenFileName(self, 'Выбрать текст', '')[0]
        writing = open(fname, mode='rt', encoding='utf-8')
        self.textEdit.setPlainText(writing.read())
        writing.close()

    def to_clearFile(self): # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self): # сохранение файла
        fname = QFileDialog.getSaveFileName(self, 'Сохраняем', '')[0]
        writing = open(fname, mode='w', encoding='utf-8')
        writing.write(self.textEdit.toPlainText())
        writing.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AdminOrUser()
    ex.show()
    sys.exit(app.exec_())