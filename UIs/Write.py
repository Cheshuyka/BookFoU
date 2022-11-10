from PyQt5 import QtCore, QtGui, QtWidgets


class WriteUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1123, 916)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(0, 50, 1121, 871))
        self.textEdit.setObjectName("textEdit")
        self.save = QtWidgets.QPushButton(Form)
        self.save.setGeometry(QtCore.QRect(0, 0, 111, 51))
        self.save.setObjectName("save")
        self.opening = QtWidgets.QPushButton(Form)
        self.opening.setGeometry(QtCore.QRect(110, 0, 111, 51))
        self.opening.setObjectName("opening")
        self.clear = QtWidgets.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(220, 0, 111, 51))
        self.clear.setObjectName("clear")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.save.setText(_translate("Form", "Save"))
        self.opening.setText(_translate("Form", "Open"))
        self.clear.setText(_translate("Form", "Clear"))
