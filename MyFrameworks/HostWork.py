from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QRadioButton, QTableWidgetItem
from PyQt5.QtWidgets import QLabel, QTableWidget, QMessageBox
import wikipedia
import warnings
from PyQt5.QtGui import QPixmap
from MyFrameworks.ShowResult import Result
from MyFrameworks.TextWindows import *
from MyFrameworks.WorkWithDBs import *
from MyFrameworks.WorkWithFiles import WorkWithFiles
import shutil
import sqlite3
from MyFrameworks.Errors import *
from PyQt5.QtCore import Qt


class AddBook(QWidget):  # интерфейс владельца
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/AddBook.ui', self)
        self.chooseCover_btn.clicked.connect(self.chooseCover)
        self.chooseText_btn.clicked.connect(self.chooseText)
        self.workerFiles = WorkWithFiles()
        self.addBook_btn.clicked.connect(self.addBook)
        self.cover = None
        self.text = None

    def chooseCover(self):
        try:
            self.cover = self.workerFiles.OpenFiles(type='Картинка')
            self.image.setPixmap(QPixmap(self.cover))
        except FileNotFoundError:
            pass

    def addBook(self):
        try:
            name = self.nameEdit.text()
            author = self.authorEdit.text()
            if self.cover is None:
                raise Exception('Картинка не указана')
            if name == '':
                raise Exception('Не указано название книги')
            if author == '':
                raise Exception('Не указан ID автора')
            con = sqlite3.connect('DBs/Authors_db.sqlite')
            cur = con.cursor()
            author = cur.execute("""SELECT id FROM Authors
                            WHERE id = ?""", (int(author),)).fetchall()
            con.close()
            if not(author):
                raise Exception('Автор не найден. Проверьте id, либо добавьте автора')
            author = author[0][0]
            con = sqlite3.connect('DBs/Books_db.sqlite')
            cur = con.cursor()
            bookID = str(cur.execute("""SELECT MAX(id) FROM Books""").fetchone()[0] + 1)
            con.close()
            con = sqlite3.connect('DBs/Books_db.sqlite')
            cur = con.cursor()
            cur.execute("""INSERT INTO Books(name, author, textLink, coverLink, btnName)
                VALUES(?, ?, ?, ?, ?)""", (name, author, f'texts/{bookID}.txt', f'covers/{bookID}.jpg', bookID))
            con.commit()
            con.close()
            shutil.copyfile(self.cover, f'covers/{bookID}.jpg')
            shutil.copyfile(self.text, f'texts/{bookID}.txt')
            self.close()
        except ValueError:
            self.w = ErrorDialog('ID автора не целое число')
            self.w.show()
        except sqlite3.IntegrityError:
            self.w = ErrorDialog('Такая книга уже существует')
            self.w.show()

    def chooseText(self):
        try:
            self.text = self.workerFiles.OpenFiles(type='Текст', to_return='Имя')
            self.chooseText_btn.setStyleSheet('background-color: lightgreen; color: white')
        except FileNotFoundError:
            pass


class AddAuthor(QWidget):  # интерфейс владельца
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/AddAuthor.ui', self)
        self.addAuthorButton.clicked.connect(self.addAuthor)

    def addAuthor(self):
        try:
            author = self.authorEdit.text()
            if author == '':
                raise Exception('Не указан автор')
            con = sqlite3.connect('DBs/Authors_db.sqlite')
            cur = con.cursor()
            authorFind = cur.execute("""SELECT id FROM Authors
                            WHERE name = ?""", (author,)).fetchall()
            con.close()
            if authorFind:
                raise Exception('Автор уже существует')
            con = sqlite3.connect('DBs/Authors_db.sqlite')
            cur = con.cursor()
            cur.execute("""INSERT INTO Authors(name) VALUES(?)""", (author, ))
            con.commit()
            con.close()
        except Exception as e:
            self.w = ErrorDialog(e.__str__())
            self.w.show()


class AddEssay(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/AddEssay.ui', self)
        self.openTextButton.clicked.connect(self.openFile)
        self.addTextButton.clicked.connect(self.addText)
        self.workerFiles = WorkWithFiles()

    def openFile(self):
        self.textEdit.setPlainText(self.workerFiles.OpenFiles())

    def addText(self):
        n = 0
        while True:
            try:
                n += 1
                f = open(f'Essays/Essay {n}.txt', mode='rt', encoding='utf-8')  # если файл не найден, то прервется цикл
                f.close()
            except FileNotFoundError:
                break
        f = open(f'Essays/Essay {n}.txt', mode='w', encoding='utf-8')
        f.write(self.textEdit.toPlainText())
        f.close()
        self.close()


class AddTest(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/AddTest.ui', self)
        self.testAddTable.setRowCount(0)
        self.addQuestionButton.clicked.connect(self.addQuestion)
        self.testAddTable.resizeColumnToContents(1)

    def addQuestion(self):
        self.testAddTable.setRowCount(self.testAddTable.rowCount() + 1)

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
            if event.key() == Qt.Key_S:
                if self.validTable():
                    self.saveTest()
        elif event.key() == Qt.Key_Delete:
            self.delete_items()

    def delete_items(self):
        rows = list(set([i.row() + 1 for i in self.testAddTable.selectedItems()]))
        rows = list(map(lambda x: str(x), sorted(rows)))
        answer = QMessageBox.question(
            self, '', "Удалить вопросы на строках: " + ",".join(rows) + '?',
            QMessageBox.Yes, QMessageBox.No)
        rows = sorted(list(map(lambda x: int(x), rows)), reverse=True)
        if answer == QMessageBox.Yes:
            for row in rows:
                self.testAddTable.removeRow(row - 1)

    def saveTest(self):
        con = sqlite3.connect('DBs/Tests_db.sqlite')
        cur = con.cursor()
        res = cur.execute("""SELECT MAX(id) FROM Tests""").fetchone()[0]
        if res is None:
            res = 1
        else:
            res += 1
        f = open(f'tests/{res}.txt', mode='w', encoding='utf-8')
        for i in range(self.testAddTable.rowCount()):
            typeOfQuest = self.testAddTable.item(i, 0).text().lower()
            question = self.testAddTable.item(i, 1).text()
            correct = self.testAddTable.item(i, 3).text()
            if typeOfQuest == 'выбор':
                options = self.testAddTable.item(i, 2).text()
                f.write(f'*{question} & {options}\n')
            elif typeOfQuest == 'ответ':
                f.write(f'#{question}\n')
            f.write(f'{correct}\n')
        f.write('END')
        f.close()
        name = self.testEdit.text()
        cur.execute("""INSERT INTO Tests(testName, testLink)
        VALUES(?, ?)""", (name, f'tests/{res}.txt'))
        con.commit()
        con.close()

    def validTable(self):
        for i in range(self.testAddTable.rowCount()):
            typeOfQuest = self.testAddTable.item(i, 0).text().lower()
            question = self.testAddTable.item(i, 1).text()
            correct = self.testAddTable.item(i, 3).text().lower()
            if not(correct):
                return False
            if not(question):
                return False
            if typeOfQuest == 'выбор':
                options = self.testAddTable.item(i, 2).text().lower()
                if correct not in options:
                    return False
                if ';' not in options:
                    return False
            elif typeOfQuest == 'ответ':
                continue
            else:
                return False
        return True