from PyQt5 import uic
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QGroupBox
from PyQt5.QtWidgets import QDialog
import sqlite3
from MyFrameworks.Interfaces import UserInterface, HostInterface
from MyFrameworks.Errors import *


class PasswordCheck(QDialog):  # проверка пользователя
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
            assert result  # пользователь найден
            assert result[1] == password  # пароль правильный
            if self.sender().text() == 'удалить пользователя':
                con = sqlite3.connect("DBs/Users_db.sqlite")
                cur = con.cursor()
                result = cur.execute("""DELETE FROM Users
                WHERE login = ?""", (login,))  # удаляем пользователя
                con.commit()
                con.close()
                self.w = Enter()  # открываем окно входа
                self.w.show()
                self.close()
            else:
                self.w = UserInterface()  # открытие окна пользователя
                self.w.show()
                self.close()
        except AssertionError:
            self.Error_lbl.setText('Логин или пароль некорректны.\nПовторите попытку')
            self.passEdit.clear()


class Enter(QDialog):  # окно для входа в программу
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/Enter.ui', self)
        self.AddUser.clicked.connect(self.add)

        self.groupBox = QGroupBox()  # создаем поле для вывода всех аккаунтов
        self.h = QVBoxLayout()
        self.groupBox.setLayout(self.h)
        self.scrollArea.setWidget(self.groupBox)
        self.commandLinkButton.clicked.connect(self.openHostCheck)

        con = sqlite3.connect("DBs/Users_db.sqlite")  # получение списка логинов
        check = con.cursor()
        result = check.execute("""SELECT login FROM Users""").fetchall()
        for i in result:  # вывод логинов
            btn = QPushButton(i[0])
            btn.clicked.connect(self.check)
            self.h.addWidget(btn)

    def check(self):  # открытие окна для проверки пароля
        self.w = PasswordCheck(self.sender().text())
        self.w.open()
        self.close()

    def add(self):  # добавление нового аккаунта
        self.w = UserAdd()
        self.w.show()
        self.close()

    def openHostCheck(self):
        self.w = HostCheck()
        self.w.show()
        self.close()

class UserAdd(QDialog):  # окно добавления пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/UserAdd.ui', self)
        self.check_btn.clicked.connect(self.add)

    def add(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()
        repeat = self.passRepeat.text()
        try:
            assert password == repeat  # пароли совпадают
            if not(password):  # если пароль пуст
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
            assert not(result)  # проверка на то, что логин не используется
        except AssertionError:
            self.Error_lbl.setText('Логин уже используется.\nПовторите попытку')
            return
        cur = con.cursor()
        cur.execute("""INSERT INTO Users(login, password)
        VALUES(?, ?)""", (login, password))  # добавляем логин и пароль в БД
        con.commit()
        con.close()
        self.w = UserInterface()  # открываем окно пользователя
        self.w.show()
        self.close()


class HostCheck(QDialog):  # проверка пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/HostCheck.ui', self)
        self.enterButton.clicked.connect(self.check)

    def check(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()
        key = self.keyEdit.text()
        con = sqlite3.connect("DBs/Hosts_db.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Hosts
                    WHERE login = ?""", (login,)).fetchone()
        try:
            if not(result):
                raise LoginNotFound()
            if key != result[2]:
                raise KeyError
            if not(result[1]):
                cur.execute("""UPDATE Hosts
                SET password = ?
                WHERE login = ?""", (password, login))
                con.commit()
            elif result[1] != password:
                raise PasswordError
            con.close()
            self.w = HostInterface()
            self.w.show()
            self.close()
        except LoginNotFound as login:
            self.error_lbl.setText(login.__str__())
        except KeyError as key:
            self.error_lbl.setText(key.__str__())
        except PasswordError as password:
            self.error_lbl.setText(password.__str__())