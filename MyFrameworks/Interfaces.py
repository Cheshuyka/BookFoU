from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QRadioButton
from PyQt5.QtWidgets import QLabel
import wikipedia
import warnings
from PyQt5.QtGui import QPixmap
import sqlite3
from MyFrameworks.ShowResult import Result
from MyFrameworks.TextWindows import *


warnings.catch_warnings()
warnings.simplefilter("ignore")


class UserInterface(QMainWindow):  # интерфейс пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/User.ui', self)
        self.wikiGet.clicked.connect(self.wiki)
        wikipedia.set_lang('ru')  # ставим язык для Википедии

        self.group = QGroupBox()  # подготавливаем поле для вывода книг
        self.h = QVBoxLayout()
        self.group.setLayout(self.h)
        self.scrollArea.setWidget(self.group)

        self.toWriteNotes.clicked.connect(self.note)
        self.toWriteEssay.clicked.connect(self.essay)
        self.find_btn.clicked.connect(self.findBooks)

        self.v = QVBoxLayout()
        self.scrollTests.setLayout(self.v)
        self.findTest_btn.clicked.connect(self.findTests)

        self.findBooks()  # выводим все книги
        self.findTests()  # выводим все тесты

    def findBooks(self):  # вывод книг
        name = self.nameEdit.text()
        author = self.authorEdit.text()
        if name and author:  # подбираем фильтры для вывода книг
            wheres = f"WHERE name LIKE '%{name}%' AND author LIKE '%{author}%'"
        elif name:
            wheres = f"WHERE name LIKE '%{name}%'"
        elif author:
            wheres = f"WHERE author LIKE '%{author}%'"
        else:
            wheres = ''
        con = sqlite3.connect("DBs/Books_db.sqlite")  # получаем книги из БД
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM Books
                    {wheres}""").fetchall()
        con.close()
        for i in reversed(range(self.h.count())):  # очищаем место для вывода книг
            self.h.itemAt(i).widget().setParent(None)
        for book in result:
            group1 = QGroupBox()
            label = QLabel()
            im = QPixmap(book[3])
            label.setPixmap(im)  # Помещаем обложку книги в label
            v = QVBoxLayout()
            v.addWidget(label)
            name = QLabel(book[0])  # Помещаем название книги в label
            with open('DBs/alreadyRead.txt', mode='rt', encoding='utf-8') as f:
                key = list(map(lambda x: x.strip('\n'), f.readlines()))
                if book[2] in key:  # если книга уже прочитана, то название книги будет зеленым
                    name.setStyleSheet('color: darkgreen')
            v.addWidget(name)
            v.addWidget(QLabel(book[1]))  # Помещаем имя автора в label
            btn = QPushButton('Читать')
            btn.setObjectName(book[4])  # Кнопку называем ссылкой на текст (понадобится при открытии книги)
            btn.clicked.connect(self.to_openBook)
            v.addWidget(btn)
            group1.setLayout(v)
            self.h.addWidget(group1)

    def findTests(self):
        for i in reversed(range(self.v.count())):  # очищаем место для вывода книг
            self.v.itemAt(i).widget().setParent(None)
        name = self.testName.text()
        if name:
            wheres = f"WHERE testName LIKE '%{name}%'"
        else:
            wheres = ''
        con = sqlite3.connect("DBs/Tests_db.sqlite")  # получаем тесты из БД
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM Tests
                            {wheres}""").fetchall()
        con.close()
        for res in result:
            btn = QPushButton(res[0])
            btn.setObjectName(res[1])
            btn.clicked.connect(self.show_test)
            self.v.addWidget(btn)

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

    def note(self):  # открытие окна для редактирования заметок
        self.write = WriteWindow()
        self.write.show()

    def essay(self):  # открытие окна для написания сочинений
        self.w = WriteEssay()

    def show_test(self):
        name = self.sender().objectName()
        self.w = Test(name)
        self.w.show()


class Test(QWidget):
    def __init__(self, file):
        super().__init__()
        uic.loadUi('UIs/Test.ui', self)
        self.h = QVBoxLayout()
        self.answer_btn.clicked.connect(self.next)
        self.answer_btn.setStyleSheet('background-color: lightgreen; color: white')
        self.answer_lbl = QLineEdit()
        self.groupBox.setLayout(self.h)
        self.correct = 0
        self.skipped = 0

        f = open(file, mode="rt", encoding='utf-8')
        self.key = list(map(lambda x: x.strip('\n'), f.readlines()))
        f.close()
        self.all = (len(self.key) - 1) // 2
        self.percent = 100 // self.all
        self.progress = 0
        self.show_test()

    def show_test(self):
        self.progressBar.setValue(self.progress)
        for i in reversed(range(self.h.count())):
            self.h.itemAt(i).widget().setParent(None)
        question = self.key[0]
        if question[0] == '#':
            self.question.setPlainText(question[1:])
            self.h.addWidget(QLabel('Введите ответ:'))
            self.h.addWidget(self.answer_lbl)
        elif question[0] == '*':
            question = question[1:].split(' & ')
            question, options = question[0], question[1].split(';')
            self.question.setPlainText(question)
            for i in options:
                btn = QRadioButton(i)
                self.h.addWidget(btn)

    def next(self):
        self.progress += self.percent
        type = self.key[0][0]
        answer = None
        if type == '#':
            answer = self.answer_lbl.text()
        elif type == '*':
            for btn in self.groupBox.findChildren(QRadioButton):
                if btn.isChecked():
                    answer = btn.text()
        try:
            assert answer is None or answer == ''
            self.skipped += 1
        except AssertionError:
            pass
        try:
            assert answer == self.key[1]
            self.correct += 1
        except AssertionError:
            pass
        self.key = self.key[2:]
        if self.key[0] == 'END':
            self.w = Result(self.correct, self.all - self.correct - self.skipped, self.skipped)
            self.w.show()
            self.close()
        else:
            self.show_test()