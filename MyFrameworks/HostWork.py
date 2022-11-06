from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QRadioButton, QTableWidgetItem
from PyQt5.QtWidgets import QLabel
import wikipedia
import warnings
from PyQt5.QtGui import QPixmap
from MyFrameworks.ShowResult import Result
from MyFrameworks.TextWindows import *
from MyFrameworks.WorkWithDBs import *


class AddBook(QWidget):  # интерфейс владельца
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/AddBook.ui', self)