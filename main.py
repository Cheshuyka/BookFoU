import sys
from PyQt5.QtWidgets import QApplication
from MyFrameworks.EnterApp import Enter


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Enter()
    ex.show()
    sys.exit(app.exec_())
