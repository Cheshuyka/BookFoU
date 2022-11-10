from PyQt5 import QtCore, QtGui, QtWidgets
from backgrounds import enterBack


class UserCheckUI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1040, 866)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.loginEdit = QtWidgets.QLineEdit(Dialog)
        self.loginEdit.setGeometry(QtCore.QRect(310, 260, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loginEdit.setFont(font)
        self.loginEdit.setStyleSheet("QLineEdit#loginEdit {\n"
"border: none;\n"
"border-bottom: 2px solid rgb(0, 32, 148);\n"
"border-top: 2px solid rgb(0, 32, 148);\n"
"background-color: rgba(9, 9, 9, 0);\n"
"color: rgba(255, 255, 255, 255);\n"
"}")
        self.loginEdit.setText("")
        self.loginEdit.setObjectName("loginEdit")
        self.passEdit = QtWidgets.QLineEdit(Dialog)
        self.passEdit.setGeometry(QtCore.QRect(310, 380, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passEdit.setFont(font)
        self.passEdit.setStyleSheet("QLineEdit#passEdit {\n"
"border: none;\n"
"border-bottom: 2px solid rgb(0, 32, 148);\n"
"border-top: 2px solid rgb(0, 32, 148);\n"
"background-color: rgba(9, 9, 9, 0);\n"
"color: rgba(255, 255, 255, 255);\n"
"}")
        self.passEdit.setText("")
        self.passEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passEdit.setObjectName("passEdit")
        self.check_btn = QtWidgets.QPushButton(Dialog)
        self.check_btn.setGeometry(QtCore.QRect(350, 540, 351, 51))
        self.check_btn.setMinimumSize(QtCore.QSize(351, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.check_btn.setFont(font)
        self.check_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.check_btn.setStyleSheet("QPushButton#check_btn {\n"
"color: rgb(255, 255, 255);\n"
"border: 2px Solid rgb(255, 255, 255);\n"
"background-color: none\n"
"}\n"
"QPushButton#check_btn:hover {\n"
"color: rgb(255, 255, 255);\n"
"border: 5px Solid rgb(255, 255, 255);\n"
"background-color: none;\n"
"}")
        self.check_btn.setObjectName("check_btn")
        self.delete_btn = QtWidgets.QPushButton(Dialog)
        self.delete_btn.setGeometry(QtCore.QRect(350, 610, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.delete_btn.setFont(font)
        self.delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_btn.setStyleSheet("QPushButton#delete_btn {\n"
"color: rgb(255, 255, 255);\n"
"border: 2px Solid rgb(255, 255, 255);\n"
"background-color: none\n"
"}\n"
"QPushButton#delete_btn:hover {\n"
"color: rgb(255, 255, 255);\n"
"border: 5px Solid rgb(255, 255, 255);\n"
"background-color: none;\n"
"}")
        self.delete_btn.setObjectName("delete_btn")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(290, 30, 471, 701))
        self.label.setStyleSheet("background-image: url(:/image/sea.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(430, 70, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white;")
        self.label_3.setObjectName("label_3")
        self.exit_btn = QtWidgets.QPushButton(Dialog)
        self.exit_btn.setGeometry(QtCore.QRect(700, 40, 51, 51))
        self.exit_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UIs\\../../../../Desktop/exit_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_btn.setIcon(icon)
        self.exit_btn.setIconSize(QtCore.QSize(60, 60))
        self.exit_btn.setObjectName("exit_btn")
        self.label.raise_()
        self.loginEdit.raise_()
        self.passEdit.raise_()
        self.check_btn.raise_()
        self.delete_btn.raise_()
        self.label_3.raise_()
        self.exit_btn.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.loginEdit.setPlaceholderText(_translate("Dialog", "Логин"))
        self.passEdit.setPlaceholderText(_translate("Dialog", "Пароль"))
        self.check_btn.setText(_translate("Dialog", "Войти"))
        self.delete_btn.setText(_translate("Dialog", "Удалить пользователя"))
        self.label_3.setText(_translate("Dialog", "Авторизация"))