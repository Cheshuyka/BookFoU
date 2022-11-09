from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class ErrorDialog(QDialog):  # окно ошибки
    def __init__(self, message):
        super().__init__()
        uic.loadUi('UIs/ErrorDialog.ui', self)
        self.okButton.clicked.connect(self.close)
        self.error_lbl.setPlainText(message)