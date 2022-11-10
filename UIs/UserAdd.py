from PyQt5 import QtCore, QtGui, QtWidgets
from backgrounds import enterBack


class UserAddUI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(503, 647)
        self.loginEdit = QtWidgets.QLineEdit(Dialog)
        self.loginEdit.setGeometry(QtCore.QRect(60, 90, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loginEdit.setFont(font)
        self.loginEdit.setStyleSheet("QLineEdit#loginEdit {\n"
"border: none;\n"
"border-bottom: 2px solid rgb(3, 76, 46);\n"
"border-top: 2px solid rgb(3, 76, 46);\n"
"background-color: rgba(9, 9, 9, 0);\n"
"color: rgba(255, 255, 255, 200);\n"
"}")
        self.loginEdit.setInputMask("")
        self.loginEdit.setText("")
        self.loginEdit.setObjectName("loginEdit")
        self.passEdit = QtWidgets.QLineEdit(Dialog)
        self.passEdit.setGeometry(QtCore.QRect(60, 220, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passEdit.setFont(font)
        self.passEdit.setStyleSheet("QLineEdit#passEdit {\n"
"border: none;\n"
"border-bottom: 2px solid rgb(3, 76, 46);\n"
"border-top: 2px solid rgb(3, 76, 46);\n"
"background-color: rgba(9, 9, 9, 0);\n"
"color: rgba(255, 255, 255, 200);\n"
"}")
        self.passEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passEdit.setObjectName("passEdit")
        self.check_btn = QtWidgets.QPushButton(Dialog)
        self.check_btn.setGeometry(QtCore.QRect(80, 480, 351, 51))
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UIs\\QLineEdit#loginEdit {"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.check_btn.setIcon(icon)
        self.check_btn.setObjectName("check_btn")
        self.Error_lbl = QtWidgets.QLabel(Dialog)
        self.Error_lbl.setGeometry(QtCore.QRect(150, 650, 211, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Error_lbl.setFont(font)
        self.Error_lbl.setStyleSheet("color: white;")
        self.Error_lbl.setText("")
        self.Error_lbl.setObjectName("Error_lbl")
        self.passRepeat = QtWidgets.QLineEdit(Dialog)
        self.passRepeat.setGeometry(QtCore.QRect(60, 350, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passRepeat.setFont(font)
        self.passRepeat.setStyleSheet("QLineEdit#passRepeat {\n"
"border: none;\n"
"border-bottom: 2px solid rgb(3, 76, 46);\n"
"border-top: 2px solid rgb(3, 76, 46);\n"
"background-color: rgba(9, 9, 9, 0);\n"
"color: rgba(255, 255, 255, 200);\n"
"}")
        self.passRepeat.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passRepeat.setObjectName("passRepeat")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 471, 621))
        self.label.setStyleSheet("background-image: url(:/image/mountains.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.exitButton = QtWidgets.QPushButton(Dialog)
        self.exitButton.setGeometry(QtCore.QRect(410, 20, 61, 61))
        self.exitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("UIs\\../../../../Desktop/exit_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon1)
        self.exitButton.setIconSize(QtCore.QSize(60, 60))
        self.exitButton.setObjectName("exitButton")
        self.label.raise_()
        self.loginEdit.raise_()
        self.passEdit.raise_()
        self.check_btn.raise_()
        self.Error_lbl.raise_()
        self.passRepeat.raise_()
        self.exitButton.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.loginEdit.setPlaceholderText(_translate("Dialog", "Логин"))
        self.passEdit.setPlaceholderText(_translate("Dialog", "Пароль"))
        self.check_btn.setText(_translate("Dialog", "Зарегистрироваться"))
        self.passRepeat.setPlaceholderText(_translate("Dialog", "Повторить пароль"))