import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QGroupBox
from PyQt5.QtWidgets import QLabel, QWidget, QDialog
import wikipedia
import warnings
from PyQt5.QtGui import QPixmap
import sqlite3
from WorkWithFiles import WorkWithFiles
from random import choice

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

        self.findBooks()  # выводим все книги

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
        self.w = WriteEssayWindow()
        self.w.show()


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
            self.loginEdit.clear()


class ReadWindow(QWidget):  # окно для открытия книги
    def __init__(self, file_name, text_name):
        super().__init__()
        uic.loadUi('UIs/TEXT.ui', self)
        self.file_name = file_name  # название файла с книгой
        self.workerFiles = WorkWithFiles()  # экземпляр класса с функционалом для открытия файлов
        self.save_btn.clicked.connect(self.to_save)
        text = open(self.file_name, mode='rt', encoding='utf-8')  # открытие текста книги
        key = text.read()
        self.textEdit.setPlainText(key)  # помещаем текст книги в поле для текста
        self.setWindowTitle(text_name)
        text.close()
        self.read_btn.clicked.connect(self.set_read)
        f = open('DBs/alreadyRead.txt', mode='r+', encoding='utf-8')  # открываем файл с названиями прочитанных книг
        self.key1 = list(map(lambda x: x.strip('\n'), f.readlines()))
        f.close()

        if self.file_name in self.key1:  # если книга уже прочитана
            self.read_btn.setStyleSheet('background-color: lightgreen; color: white')
            self.read_btn.setText('Прочитано')

    def to_save(self):  # сохранение книги в отдельный файл
        self.workerFiles.SaveFiles(self.textEdit.toPlainText())

    def set_read(self):
        f = open('DBs/alreadyRead.txt', mode='r+', encoding='utf-8')  # открытие файла со списком прочитанных книг
        if self.read_btn.text() == 'Не прочитано':  # если на книге еще нет отметки 'прочитано'
            self.read_btn.setStyleSheet('background-color: lightgreen; color: white')  # изменяем стиль кнопки
            self.read_btn.setText('Прочитано')
            self.key1.append(self.file_name)  # добавление книги в список прочитанных
            f.truncate(0)
            f.write('\n'.join(self.key1))
        else:  # если отметка уже есть
            self.read_btn.setStyleSheet('background-color: white; color: black')
            self.read_btn.setText('Не прочитано')
            self.key1.remove(self.file_name)  # удаление книги из списка прочитанных
            f.truncate(0)
            f.write('\n'.join(self.key1))
        f.close()


class WriteWindow(QWidget):  # окно для редактирования заметок
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE.ui', self)
        self.workerFiles = WorkWithFiles()
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)

    def to_openFile(self):  # открытие файла
        self.textEdit.setPlainText(self.workerFiles.OpenFiles())

    def to_clearFile(self):  # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self):  # сохранение файла
        self.workerFiles.SaveFiles(self.textEdit.toPlainText())


class Enter(QDialog):  # окно для входа в программу
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/Enter.ui', self)
        self.AddUser.clicked.connect(self.add)

        self.groupBox = QGroupBox()  # создаем поле для вывода всех аккаунтов
        self.h = QVBoxLayout()
        self.groupBox.setLayout(self.h)
        self.scrollArea.setWidget(self.groupBox)

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


class WriteEssayWindow(QWidget):  # окно для редактирования сочинений
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/WRITE_ESSAY.ui', self)
        self.opening.clicked.connect(self.to_openFile)
        self.clear.clicked.connect(self.to_clearFile)
        self.save.clicked.connect(self.to_saveFile)
        self.getTheme.clicked.connect(self.show_theme)
        self.openingRecent.clicked.connect(self.show_essays)
        self.workerFiles = WorkWithFiles()

    def to_openFile(self):  # открытие файла
        self.textEdit.setPlainText(self.workerFiles.OpenFiles())

    def show_theme(self):  # получение темы для сочинения
        f = open("texts/essays.txt", mode="rt", encoding='utf-8')
        key = list(map(lambda x: x.strip('\n'), f.readlines()))
        theme = choice(key)
        self.theme_lbl.setText(theme)

    def to_clearFile(self):  # очистка поля ввода
        self.textEdit.clear()

    def to_saveFile(self):  # сохранение файла
        self.textEdit.setPlainText(self.workerFiles.SaveFiles(self.textEdit.toPlainText()))

    def show_essays(self):  # TODO: сделать вывод уже написанных сочинений
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Enter()
    ex.show()
    sys.exit(app.exec_())
