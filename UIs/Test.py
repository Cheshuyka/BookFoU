from PyQt5 import QtCore, QtGui, QtWidgets


class TestUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1042, 611)
        self.answer_btn = QtWidgets.QPushButton(Form)
        self.answer_btn.setGeometry(QtCore.QRect(930, 490, 111, 41))
        self.answer_btn.setObjectName("answer_btn")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(0, 220, 1041, 271))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.question = QtWidgets.QTextEdit(Form)
        self.question.setGeometry(QtCore.QRect(0, 0, 1041, 201))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.question.setFont(font)
        self.question.setReadOnly(True)
        self.question.setObjectName("question")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(0, 540, 1041, 71))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.answer_btn.setText(_translate("Form", "Ответить!"))
        self.question.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
