from PyQt5 import QtCore, QtGui, QtWidgets


class AddBookUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(699, 783)
        self.image = QtWidgets.QLabel(Form)
        self.image.setGeometry(QtCore.QRect(20, 80, 281, 401))
        self.image.setFrameShape(QtWidgets.QFrame.Box)
        self.image.setText("")
        self.image.setObjectName("image")
        self.chooseCover_btn = QtWidgets.QPushButton(Form)
        self.chooseCover_btn.setGeometry(QtCore.QRect(320, 250, 181, 41))
        self.chooseCover_btn.setObjectName("chooseCover_btn")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 561, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.addBook_btn = QtWidgets.QPushButton(Form)
        self.addBook_btn.setGeometry(QtCore.QRect(220, 690, 181, 41))
        self.addBook_btn.setObjectName("addBook_btn")
        self.nameEdit = QtWidgets.QLineEdit(Form)
        self.nameEdit.setGeometry(QtCore.QRect(40, 530, 501, 22))
        self.nameEdit.setText("")
        self.nameEdit.setObjectName("nameEdit")
        self.chooseText_btn = QtWidgets.QPushButton(Form)
        self.chooseText_btn.setGeometry(QtCore.QRect(40, 630, 501, 41))
        self.chooseText_btn.setObjectName("chooseText_btn")
        self.authorEdit = QtWidgets.QLineEdit(Form)
        self.authorEdit.setGeometry(QtCore.QRect(40, 580, 501, 22))
        self.authorEdit.setText("")
        self.authorEdit.setObjectName("authorEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.chooseCover_btn.setText(_translate("Form", "Выбрать обложку"))
        self.label.setText(_translate("Form", "Если обложка помещается в рамки ниже, то можете ее использовать"))
        self.addBook_btn.setText(_translate("Form", "Добавить книгу"))
        self.nameEdit.setPlaceholderText(_translate("Form", "Название книги"))
        self.chooseText_btn.setText(_translate("Form", "Выбрать txt файл с текстом книги"))
        self.authorEdit.setPlaceholderText(_translate("Form", "ID автора"))
