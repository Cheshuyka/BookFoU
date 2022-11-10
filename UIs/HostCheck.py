from PyQt5 import QtCore, QtGui, QtWidgets
from backgrounds import enterBack


class HostCheckUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1039, 638)
        self.keyEdit = QtWidgets.QLineEdit(Form)
        self.keyEdit.setGeometry(QtCore.QRect(300, 340, 471, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.keyEdit.setFont(font)
        self.keyEdit.setStyleSheet("QLineEdit#keyEdit {\n"
"border: none;\n"
"border-bottom: 2px solid rgb(255, 255, 255);\n"
"border-top: 2px solid rgb(255, 255, 255);\n"
"background-color: rgba(9, 9, 9, 0);\n"
"color: rgba(255, 255, 255, 200);\n"
"}")
        self.keyEdit.setText("")
        self.keyEdit.setObjectName("keyEdit")
        self.passEdit = QtWidgets.QLineEdit(Form)
        self.passEdit.setGeometry(QtCore.QRect(300, 210, 471, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passEdit.setFont(font)
        self.passEdit.setStyleSheet("QLineEdit#passEdit {\n"
"border: none;\n"
"border-bottom: 2px solid rgb(255, 255, 255);\n"
"border-top: 2px solid rgb(255, 255, 255);\n"
"background-color: rgba(9, 9, 9, 0);\n"
"color: rgba(255, 255, 255, 200);\n"
"}")
        self.passEdit.setText("")
        self.passEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passEdit.setObjectName("passEdit")
        self.loginEdit = QtWidgets.QLineEdit(Form)
        self.loginEdit.setGeometry(QtCore.QRect(300, 80, 471, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.loginEdit.setFont(font)
        self.loginEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.loginEdit.setStyleSheet("QLineEdit#loginEdit {\n"
"border: none;\n"
"border-bottom: 2px solid rgb(255, 255, 255);\n"
"border-top: 2px solid rgb(255, 255, 255);\n"
"background-color: rgba(9, 9, 9, 0);\n"
"color: rgba(255, 255, 255, 200);\n"
"}")
        self.loginEdit.setText("")
        self.loginEdit.setObjectName("loginEdit")
        self.enterButton = QtWidgets.QPushButton(Form)
        self.enterButton.setGeometry(QtCore.QRect(340, 470, 391, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.enterButton.setFont(font)
        self.enterButton.setStyleSheet("QPushButton#enterButton {\n"
"color: rgb(255, 255, 255);\n"
"border: 2px Solid rgb(255, 255, 255);\n"
"background-color: none\n"
"}\n"
"QPushButton#enterButton:hover {\n"
"color: rgb(255, 255, 255);\n"
"border: 5px Solid rgb(255, 255, 255);\n"
"background-color: none;\n"
"}")
        self.enterButton.setObjectName("enterButton")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(250, -10, 571, 631))
        self.label_4.setStyleSheet("background-image: url(:/image/meduza.jpg);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.exitButton = QtWidgets.QPushButton(Form)
        self.exitButton.setGeometry(QtCore.QRect(760, 10, 51, 51))
        self.exitButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UIs\\../../../../Desktop/exit_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon)
        self.exitButton.setIconSize(QtCore.QSize(60, 60))
        self.exitButton.setObjectName("exitButton")
        self.label_4.raise_()
        self.keyEdit.raise_()
        self.passEdit.raise_()
        self.loginEdit.raise_()
        self.enterButton.raise_()
        self.exitButton.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.keyEdit.setPlaceholderText(_translate("Form", "Ключ активации продукта"))
        self.passEdit.setPlaceholderText(_translate("Form", "Пароль"))
        self.loginEdit.setPlaceholderText(_translate("Form", "Логин"))
        self.enterButton.setText(_translate("Form", "Зайти как владелец"))
