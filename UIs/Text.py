from PyQt5 import QtCore, QtGui, QtWidgets


class TextUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1103, 900)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(0, 40, 1101, 861))
        self.textEdit.setObjectName("textEdit")
        self.save_btn = QtWidgets.QPushButton(Form)
        self.save_btn.setGeometry(QtCore.QRect(0, 0, 181, 41))
        self.save_btn.setObjectName("save_btn")
        self.read_btn = QtWidgets.QPushButton(Form)
        self.read_btn.setGeometry(QtCore.QRect(180, 0, 211, 41))
        self.read_btn.setObjectName("read_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.save_btn.setText(_translate("Form", "Скачать книгу"))
        self.read_btn.setText(_translate("Form", "Не прочитано"))
