from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QRadioButton, QTableWidgetItem
from PyQt5.QtWidgets import QLabel
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
            shutil.copyfile(self.cover, f'covers/{bookID}.jpg')
            shutil.copyfile(self.text, f'texts/{bookID}.txt')
            con = sqlite3.connect('DBs/Books_db.sqlite')
            cur = con.cursor()
            cur.execute("""INSERT INTO Books(name, author, textLink, coverLink, btnName)
                VALUES(?, ?, ?, ?, ?)""", (name, author, f'texts/{bookID}.txt', f'covers/{bookID}.jpg', bookID))
            con.commit()
            con.close()
        except ValueError:
            self.w = ErrorDialog('ID автора не целое число')
            self.w.show()
        except Exception as e:
            self.w = ErrorDialog(e.__str__())
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