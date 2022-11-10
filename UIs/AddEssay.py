from PyQt5 import QtCore, QtGui, QtWidgets


class AddEssayUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1038, 915)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 140, 1021, 771))
        self.textEdit.setObjectName("textEdit")
        self.openTextButton = QtWidgets.QPushButton(Form)
        self.openTextButton.setGeometry(QtCore.QRect(40, 40, 151, 41))
        self.openTextButton.setObjectName("openTextButton")
        self.addTextButton = QtWidgets.QPushButton(Form)
        self.addTextButton.setGeometry(QtCore.QRect(810, 50, 141, 41))
        self.addTextButton.setStyleSheet("background-color: lightgreen;\n"
"color: white;")
        self.addTextButton.setObjectName("addTextButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.openTextButton.setText(_translate("Form", "Открыть файл"))
        self.addTextButton.setText(_translate("Form", "Добавить текст"))
