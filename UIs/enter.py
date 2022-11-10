from PyQt5 import QtCore, QtGui, QtWidgets
from backgrounds import enterBack


class EnterUI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(477, 485)
        Dialog.setStyleSheet("")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(40, 160, 391, 191))
        self.scrollArea.setStyleSheet("visible: none")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 391, 191))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.AddUser = QtWidgets.QPushButton(Dialog)
        self.AddUser.setGeometry(QtCore.QRect(60, 60, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.AddUser.setFont(font)
        self.AddUser.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.AddUser.setStyleSheet("QPushButton#AddUser {\n"
"background-color: #ecdbd1;\n"
"color: white;\n"
"}\n"
"QPushButton#AddUser:hover {\n"
"background-color: #cebdb4;\n"
"}\n"
"QPushButton#AddUser:pressed {\n"
"background-color: #cec1d8;\n"
"}")
        self.AddUser.setObjectName("AddUser")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 451, 451))
        self.label.setStyleSheet("background-image: url(:/image/enter_background.jpg);\n"
"border-radius: 50px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.host_btn = QtWidgets.QPushButton(Dialog)
        self.host_btn.setGeometry(QtCore.QRect(130, 380, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.host_btn.setFont(font)
        self.host_btn.setAutoFillBackground(False)
        self.host_btn.setStyleSheet("QPushButton#host_btn {\n"
"color: white;\n"
"border-radius:10px;\n"
"}\n"
"QPushButton#host_btn:hover{\n"
"color: #e5a00b;\n"
"}")
        self.host_btn.setObjectName("host_btn")
        self.label.raise_()
        self.scrollArea.raise_()
        self.AddUser.raise_()
        self.host_btn.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Вход"))
        self.AddUser.setText(_translate("Dialog", "Добавить пользователя"))
        self.host_btn.setText(_translate("Dialog", "Вы владелец?"))