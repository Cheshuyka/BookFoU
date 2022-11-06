from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QRadioButton, QTableWidgetItem
from PyQt5.QtWidgets import QLabel
import wikipedia
import warnings
from PyQt5.QtGui import QPixmap
from MyFrameworks.ShowResult import Result
from MyFrameworks.TextWindows import *
from MyFrameworks.WorkWithDBs import *


warnings.catch_warnings()
warnings.simplefilter("ignore")


class UserInterface(QMainWindow):  # интерфейс пользователя
    def __init__(self, login):
        super().__init__()
        uic.loadUi('UIs/User.ui', self)
        self.wikiGet.clicked.connect(self.wiki)
        wikipedia.set_lang('ru')  # ставим язык для Википедии
        self.login = login

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
        self.findMadeTest_btn.clicked.connect(self.showMadeTests)

        self.findBooks()  # выводим все книги
        self.findTests()  # выводим все тесты
        self.showMadeTests()

    def findBooks(self):  # вывод книг
        name = self.nameEdit.text()
        authorName = self.authorEdit.text()
        result = getBooks(name, authorName)
        f = open(f'UsersData/_{self.login}_ALREADYREADBOOKS.txt', mode='rt', encoding='utf-8')
        key = list(map(lambda x: x.strip('\n'), f))
        f.close()
        for i in reversed(range(self.h.count())):  # очищаем место для вывода книг
            self.h.itemAt(i).widget().setParent(None)
        for book in result:
            group1 = QGroupBox()
            label = QLabel()
            im = QPixmap(book[4])
            label.setPixmap(im)  # Помещаем обложку книги в label
            v = QVBoxLayout()
            v.addWidget(label)
            name = QLabel(book[1])  # Помещаем название книги в label
            if str(book[0]) in key:  # если книга уже прочитана, то название книги будет зеленым
                name.setStyleSheet('color: darkgreen')
            v.addWidget(name)
            v.addWidget(QLabel(book[2]))  # Помещаем имя автора в label
            btn = QPushButton('Читать')
            btn.setObjectName(book[5])  # Кнопку называем ссылкой на текст (понадобится при открытии книги)
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

    def showMadeTests(self):
        self.testsTable.setColumnCount(3)
        self.testsTable.setRowCount(0)
        name = self.madeTestName.text()
        f = open(f'UsersData/_{self.login}_ALREADYDONETESTS.txt', mode='rt', encoding='utf-8')
        result = list(filter(lambda x: name in x, list(map(lambda x: x.strip('\n'), f.readlines()))))
        s = result.copy()
        con = sqlite3.connect("DBs/Tests_db.sqlite")  # получаем тесты из БД
        cur = con.cursor()
        for i in range(len(result)):
            res = cur.execute(f"""SELECT testName FROM Tests
                        WHERE testLink = ?""", (result[i].split(':')[0], )).fetchone()
            result[i] = res[0] + ':' + result[i].split(':')[1]
        for i in range(len(result)):
            self.testsTable.setRowCount(self.testsTable.rowCount() + 1)
            res = result[i].split(':')
            self.testsTable.setItem(i, 0, QTableWidgetItem(str(res[0])))
            self.testsTable.setItem(i, 1, QTableWidgetItem(str(res[1])))
            btn = QPushButton('Выполнить')
            btn.setObjectName(s[i].split(':')[0])
            btn.clicked.connect(self.show_test)
            self.testsTable.setCellWidget(i, 2, btn)
        con.close()

    def wiki(self):  # вывод определения слова
        try:
            word = self.wikiLine.text()  # получение слова
            self.wikiText.setText(str(wikipedia.summary(word).split('\n')[0]))  # вывод определения
        except Exception:  # если слово не найдено или поле пусто
            self.wikiText.setText('определение слова не найдено')

    def to_openBook(self):  # открытие книги в отдельном окне
        result = open_book(self.sender().objectName())
        self.w = ReadWindow(result[1], result[2], result[0], self.login)
        self.w.show()

    def note(self):  # открытие окна для редактирования заметок
        self.write = WriteWindow()
        self.write.show()

    def essay(self):  # открытие окна для написания сочинений
        self.w = WriteEssay()

    def show_test(self):
        name = self.sender().objectName()
        self.w = Test(name, self.login)
        self.w.show()


class Test(QWidget):
    def __init__(self, file, login):
        super().__init__()
        uic.loadUi('UIs/Test.ui', self)
        self.login = login
        self.file = file
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
        f = open(f'UsersData/_{self.login}_ALREADYDONETESTS.txt', mode='rt', encoding='utf-8')
        self.res = list(map(lambda x: x.strip('\n'), f))
        f.close()
        self.results = list(map(lambda x: file in x, self.res))

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
            if not(self.results):
                self.results = None
            else:
                self.results = self.results[0]
            incorrect = self.all - self.correct - self.skipped
            self.w = Result(self.correct, incorrect, self.skipped, f'UsersData/_{self.login}_ALREADYDONETESTS.txt',
                            self.file)
            self.w.show()
            self.close()
        else:
            self.show_test()


class HostInterface(QMainWindow):  # интерфейс владельца
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/Host.ui', self)
        self.findBooksButton.clicked.connect(self.findBooks)
        self.addBookButton.clicked.connect(self.addBook)

    def findBooks(self):
        self.booksTable.setColumnCount(5)
        self.booksTable.setRowCount(0)
        name = self.nameEdit.text()
        authorName = self.authorEdit.text()
        result = getBooks(name, authorName)
        for i, row in enumerate(result):
            row = row[1:]
            row, btnName = row[:-2], row[4]
            self.booksTable.setRowCount(self.booksTable.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 2:
                    elem = QPushButton('Читать')
                    elem.setObjectName(btnName)
                    elem.clicked.connect(self.to_openBook)
                    self.booksTable.setCellWidget(i, j, elem)
                else:
                    self.booksTable.setItem(i, j, QTableWidgetItem(str(elem)))

    def addBook(self):
        pass

    def to_openBook(self):
        result = open_book(self.sender().objectName())
        self.w = ReadWindow(result[1], result[2], result[0], None)
        self.w.show()