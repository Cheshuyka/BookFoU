from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class LoginError(Exception):
    pass


class PasswordError(Exception):
    pass


class KeyError(Exception):
    pass


class ErrorDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        uic.loadUi('UIs/ErrorDialog.ui', self)
        self.okButton.clicked.connect(self.close)
        self.error_lbl.setPlainText(message)