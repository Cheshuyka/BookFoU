from PyQt5.QtWidgets import QDialog
from UIs.ErrorDialog import ErrorDialogUI


class ErrorDialog(QDialog, ErrorDialogUI):  # окно ошибки
    def __init__(self, message):
        super().__init__()
        self.setupUi(self)
        self.okButton.clicked.connect(self.close)
        self.error_lbl.setPlainText(message)