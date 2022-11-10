from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QRadioButton, QTableWidgetItem
from PyQt5.QtWidgets import QLabel
import wikipedia
import warnings
from MyFrameworks.ShowResult import Result
from MyFrameworks.WorkWithDBs import *
from MyFrameworks.HostWork import *
import os
from UIs.User import UserUI
from UIs.Test import TestUI
from UIs.Host import HostUI


warnings.catch_warnings()
warnings.simplefilter("ignore")


class UserInterface(QMainWindow, UserUI):  # интерфейс пользователя
    def __init__(self, login):
        super().__init__()
        self.setupUi(self)
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
        result = cur.execute(f"""SELECT testName, testLink FROM Tests
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
        self.w = WriteEssay(self.login)

    def show_test(self):
        name = self.sender().objectName()
        self.w = Test(name, self.login)
        self.w.show()


class Test(QWidget, TestUI):  # окно теста
    def __init__(self, file, login):
        super().__init__()
        self.setupUi(self)
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

        self.all = (len(self.key) - 1) // 2  # количество вопросов
        self.percent = 100 // self.all  # кол-во процентов за один вопрос
        self.progress = 0  # для progressBar
        self.show_test()

    def show_test(self):  # показ вопроса теста
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

    def next(self):  # обработка ответов
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
            assert answer
            assert answer.lower() == self.key[1].lower()
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


class HostInterface(QMainWindow, HostUI):  # интерфейс владельца
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.findBooksButton.clicked.connect(self.findBooks)
        self.addBookButton.clicked.connect(self.addBook)
        self.findAuthorButton.clicked.connect(self.findAuthors)
        self.addAuthorButton.clicked.connect(self.addAuthor)
        self.findUserButton.clicked.connect(self.findUsers)
        self.addEssayButton.clicked.connect(self.addEssay)
        self.addTestButton.clicked.connect(self.addTest)
        self.findBooks()
        self.findAuthors()
        self.findUsers()
        self.findEssays()

    def findBooks(self):  # вывод книг
        self.booksTable.setColumnCount(3)
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

    def addBook(self):  # добавление книги
        self.w = AddBook()
        self.w.show()

    def addAuthor(self):  # добавление автора
        self.w = AddAuthor()
        self.w.show()

    def to_openBook(self):  # открытие книги
        result = open_book(self.sender().objectName())
        self.w = ReadWindow(result[1], result[2], result[0], None)
        self.w.show()

    def findAuthors(self):  # найти атвора
        self.authorsTable.setColumnCount(2)
        self.authorsTable.setRowCount(0)
        authorName = self.authorNameEdit.text()
        if authorName == '':
            wheres = ''
        else:
            wheres = f"WHERE name LIKE '%{authorName}%'"
        con = sqlite3.connect('DBs/Authors_db.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM Authors
                    {wheres}""").fetchall()
        con.close()
        for i, row in enumerate(result):
            self.authorsTable.setRowCount(self.authorsTable.rowCount() + 1)
            for j, elem in enumerate(row):
                self.authorsTable.setItem(i, j, QTableWidgetItem(str(elem)))

    def findUsers(self):  # найти пользователей
        self.usersTable.setColumnCount(3)
        self.usersTable.setRowCount(0)
        user = self.userEdit.text()
        if user == '':
            wheres = ''
        else:
            wheres = f"WHERE login LIKE '%{user}%'"
        con = sqlite3.connect('DBs/Users_db.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT login, password FROM Users
                            {wheres}""").fetchall()
        con.close()
        for i, row in enumerate(result):
            self.usersTable.setRowCount(self.usersTable.rowCount() + 1)
            self.usersTable.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.usersTable.setItem(i, 1, QTableWidgetItem(str(row[1])))
            btn = QPushButton('Удалить')
            btn.setObjectName(row[0])
            btn.clicked.connect(self.deleteUser)
            self.usersTable.setCellWidget(i, 2, btn)

    def deleteUser(self):  # удаление пользователя
        con = sqlite3.connect("DBs/Users_db.sqlite")
        cur = con.cursor()
        cur.execute("""DELETE FROM Users
        WHERE login = ?""", (self.sender().objectName(), ))  # удаляем пользователя
        con.commit()
        con.close()
        os.remove(f'UsersData/_{self.sender().objectName()}_ALREADYREADBOOKS.txt')
        os.remove(f'UsersData/_{self.sender().objectName()}_ALREADYDONETESTS.txt')
        os.remove(f'UsersData/_{self.sender().objectName()}_LASTWRITTEN.txt')

    def findEssays(self):  # поиск текстов сочинений
        self.essaysTable.setColumnCount(1)
        self.essaysTable.setRowCount(0)
        n = 0
        while True:
            try:
                n += 1
                f = open(f'Essays/Essay {n}.txt', mode='rt', encoding='utf-8')  # если файл не найден, то прервется цикл
                f.close()
                self.essaysTable.setRowCount(self.essaysTable.rowCount() + 1)
                btn = QPushButton(f'Сочинение {n}')
                btn.clicked.connect(self.openEssay)
                btn.setObjectName(f'Essays/Essay {n}.txt')
                self.essaysTable.setCellWidget(n - 1, 0, btn)
            except FileNotFoundError:
                break

    def openEssay(self):  # открытие текста сочинения
        f = open(self.sender().objectName(), mode='rt', encoding='utf-8')
        key = f.read()
        f.close()
        self.essayText.setPlainText(key)

    def addEssay(self):  # добавление задания для сочинения
        self.w = AddEssay()
        self.w.show()

    def addTest(self):  # добавление теста
        self.w = AddTest()
        self.w.show()