from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QGroupBox
import sqlite3
from MyFrameworks.Interfaces import UserInterface, HostInterface
from MyFrameworks.Errors import *
from backgrounds.enterBack import *
import os


class PasswordCheck(QDialog):  # проверка пользователя
    def __init__(self, login):
        super().__init__()
        uic.loadUi('UIs/UserCheck.ui', self)
        self.check_btn.clicked.connect(self.check)
        self.loginEdit.setText(login)
        self.delete_btn.clicked.connect(self.check)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.exit_btn.clicked.connect(self.exit)

    def check(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()
        con = sqlite3.connect("DBs/Users_db.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Users
                    WHERE login = ?""", (login,)).fetchone()
        con.close()
        try:
            if not(result): # пользователь не найден
                raise Exception('Пользователь не найден')
            if result[1] != password:  # неверный пароль
                raise Exception('Неверный пароль')
            if self.sender().text() == 'Удалить пользователя':
                con = sqlite3.connect("DBs/Users_db.sqlite")
                cur = con.cursor()
                result = cur.execute("""DELETE FROM Users
                WHERE login = ?""", (login,))  # удаляем пользователя
                con.commit()
                con.close()
                self.w = Enter()  # открываем окно входа
                self.w.show()
                os.remove(f'UsersData/_{login}_ALREADYREADBOOKS.txt')
                os.remove(f'UsersData/_{login}_ALREADYDONETESTS.txt')
                os.remove(f'UsersData/_{login}_LASTWRITTEN.txt')
                self.close()
            else:
                self.w = UserInterface(login)  # открытие окна пользователя
                self.w.show()
                self.close()
        except ValueError:
            pass
        except Exception as e:
            self.w = ErrorDialog(e.__str__())
            self.w.show()

    def exit(self):
        self.w = Enter()
        self.w.show()
        self.close()


class Enter(QDialog):  # окно для входа в программу
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/Enter.ui', self)
        self.AddUser.clicked.connect(self.add)

        self.groupBox = QGroupBox()  # создаем поле для вывода всех аккаунтов
        self.h = QVBoxLayout()
        self.groupBox.setLayout(self.h)
        self.scrollArea.setWidget(self.groupBox)
        self.host_btn.clicked.connect(self.openHostCheck)

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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.exitButton.clicked.connect(self.exit)

    def add(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()
        repeat = self.passRepeat.text()
        try:
            if not(password):  # если пароль пуст
                raise Exception('Пароль пуст')
            if not(login):
                raise Exception('Логин пуст')
            if password != repeat:  # пароли не совпадают
                raise Exception('Пароли не совпадают')
            con = sqlite3.connect("DBs/Users_db.sqlite")
            check = con.cursor()
            result = check.execute("""SELECT * FROM Users
                        WHERE login = ?""", (login,)).fetchall()
            if result:  # проверка на то, что логин не используется
                raise Exception('Логин уже используется')
            cur = con.cursor()
            cur.execute("""INSERT INTO Users(login, password)
            VALUES(?, ?)""", (login, password))  # добавляем логин и пароль в БД
            con.commit()
            con.close()
            f = open(f'UsersData/_{login}_ALREADYREADBOOKS.txt', mode='w', encoding='utf-8')
            f.close()
            f = open(f'UsersData/_{login}_ALREADYDONETESTS.txt', mode='w', encoding='utf-8')
            f.close()
            f = open(f'UsersData/_{login}_LASTWRITTEN.txt', mode='w', encoding='utf-8')
            f.write('1')
            f.close()
            self.w = UserInterface(login)  # открываем окно пользователя
            self.w.show()
            self.close()
        except Exception as e:
            self.w = ErrorDialog(e.__str__())
            self.w.show()

    def exit(self):
        self.w = Enter()
        self.w.show()
        self.close()


class HostCheck(QDialog):  # проверка пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/HostCheck.ui', self)
        self.enterButton.clicked.connect(self.check)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.exitButton.clicked.connect(self.exit)

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
                raise Exception('Владелец не найден')
            if key != result[2]:
                raise KeyError('Ошибка ключа активации продукта')
            if not(result[1]):
                cur.execute("""UPDATE Hosts
                SET password = ?
                WHERE login = ?""", (password, login))
                con.commit()
            elif result[1] != password:
                raise Exception('Неверный пароль')
            con.close()
            self.w = HostInterface()
            self.w.show()
            self.close()
        except Exception as e:
            self.w = ErrorDialog(e.__str__())
            self.w.show()

    def exit(self):
        self.w = Enter()
        self.w.show()
        self.close()