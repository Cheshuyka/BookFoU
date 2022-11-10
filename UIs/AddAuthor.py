from PyQt5 import QtCore, QtGui, QtWidgets


class AddAuthorUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(656, 157)
        self.authorEdit = QtWidgets.QLineEdit(Form)
        self.authorEdit.setGeometry(QtCore.QRect(30, 40, 581, 22))
        self.authorEdit.setReadOnly(False)
        self.authorEdit.setObjectName("authorEdit")
        self.addAuthorButton = QtWidgets.QPushButton(Form)
        self.addAuthorButton.setGeometry(QtCore.QRect(30, 110, 581, 28))
        self.addAuthorButton.setObjectName("addAuthorButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.authorEdit.setPlaceholderText(_translate("Form", "Автор"))
        self.addAuthorButton.setText(_translate("Form", "Добавить автора"))
