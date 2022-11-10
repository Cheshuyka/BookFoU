from PyQt5 import QtCore, QtGui, QtWidgets


class HostUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1034, 917)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1031, 861))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.findBooksButton = QtWidgets.QPushButton(self.tab)
        self.findBooksButton.setGeometry(QtCore.QRect(520, 20, 211, 28))
        self.findBooksButton.setObjectName("findBooksButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 511, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.authorEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.authorEdit.setObjectName("authorEdit")
        self.verticalLayout.addWidget(self.authorEdit)
        self.nameEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout.addWidget(self.nameEdit)
        self.booksTable = QtWidgets.QTableWidget(self.tab)
        self.booksTable.setGeometry(QtCore.QRect(0, 150, 1021, 681))
        self.booksTable.setRowCount(0)
        self.booksTable.setObjectName("booksTable")
        self.booksTable.setColumnCount(0)
        self.addBookButton = QtWidgets.QPushButton(self.tab)
        self.addBookButton.setGeometry(QtCore.QRect(390, 110, 241, 28))
        self.addBookButton.setObjectName("addBookButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.authorNameEdit = QtWidgets.QLineEdit(self.tab_3)
        self.authorNameEdit.setGeometry(QtCore.QRect(10, 20, 509, 22))
        self.authorNameEdit.setObjectName("authorNameEdit")
        self.authorsTable = QtWidgets.QTableWidget(self.tab_3)
        self.authorsTable.setGeometry(QtCore.QRect(0, 150, 1031, 681))
        self.authorsTable.setRowCount(0)
        self.authorsTable.setObjectName("authorsTable")
        self.authorsTable.setColumnCount(0)
        self.addAuthorButton = QtWidgets.QPushButton(self.tab_3)
        self.addAuthorButton.setGeometry(QtCore.QRect(390, 80, 241, 28))
        self.addAuthorButton.setObjectName("addAuthorButton")
        self.findAuthorButton = QtWidgets.QPushButton(self.tab_3)
        self.findAuthorButton.setGeometry(QtCore.QRect(580, 20, 211, 28))
        self.findAuthorButton.setObjectName("findAuthorButton")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.userEdit = QtWidgets.QLineEdit(self.tab_4)
        self.userEdit.setGeometry(QtCore.QRect(10, 20, 509, 22))
        self.userEdit.setObjectName("userEdit")
        self.findUserButton = QtWidgets.QPushButton(self.tab_4)
        self.findUserButton.setGeometry(QtCore.QRect(650, 20, 211, 28))
        self.findUserButton.setObjectName("findUserButton")
        self.usersTable = QtWidgets.QTableWidget(self.tab_4)
        self.usersTable.setGeometry(QtCore.QRect(0, 80, 1031, 751))
        self.usersTable.setRowCount(0)
        self.usersTable.setObjectName("usersTable")
        self.usersTable.setColumnCount(0)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.essaysTable = QtWidgets.QTableWidget(self.tab_5)
        self.essaysTable.setGeometry(QtCore.QRect(0, 70, 1031, 331))
        self.essaysTable.setObjectName("essaysTable")
        self.essaysTable.setColumnCount(0)
        self.essaysTable.setRowCount(0)
        self.addEssayButton = QtWidgets.QPushButton(self.tab_5)
        self.addEssayButton.setGeometry(QtCore.QRect(400, 20, 201, 28))
        self.addEssayButton.setObjectName("addEssayButton")
        self.essayText = QtWidgets.QTextEdit(self.tab_5)
        self.essayText.setGeometry(QtCore.QRect(0, 430, 1031, 401))
        self.essayText.setObjectName("essayText")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.addTestButton = QtWidgets.QPushButton(self.tab_2)
        self.addTestButton.setGeometry(QtCore.QRect(20, 230, 981, 291))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.addTestButton.setFont(font)
        self.addTestButton.setObjectName("addTestButton")
        self.textEdit = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 1031, 211))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1034, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.findBooksButton.setText(_translate("MainWindow", "Найти"))
        self.authorEdit.setPlaceholderText(_translate("MainWindow", "Автор"))
        self.nameEdit.setPlaceholderText(_translate("MainWindow", "Название"))
        self.addBookButton.setText(_translate("MainWindow", "Добавить книгу"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Books"))
        self.authorNameEdit.setPlaceholderText(_translate("MainWindow", "Автор"))
        self.addAuthorButton.setText(_translate("MainWindow", "Добавить автора"))
        self.findAuthorButton.setText(_translate("MainWindow", "Найти"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Authors"))
        self.userEdit.setPlaceholderText(_translate("MainWindow", "Пользователь"))
        self.findUserButton.setText(_translate("MainWindow", "Найти"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Users"))
        self.addEssayButton.setText(_translate("MainWindow", "Добавить текст для анализа"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Essays"))
        self.addTestButton.setText(_translate("MainWindow", "Добавить тест"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Подсказки по добавлению тестов</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">В первой графе напишите ответ или выбор.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Во второй: вопрос. Обязательно последним символом поставьте знак препинания!</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">В третьей: варианты ответа (если нужно). Перечислите их через знак &quot;;&quot;. </span><span style=\" font-size:10pt; font-weight:600; text-decoration: underline;\">БЕЗ ПРОБЕЛОВ.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">В четвертой: правильный вариант ответа.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Название теста не должно быть использовано.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Пройти тест Вы можете, если зайдете в систему как пользователь.</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tests"))
