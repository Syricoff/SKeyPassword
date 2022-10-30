import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon

from dialogs import AddPassword, AboutProgram
from ui.ui_MainWindow import Ui_MainWindow as Main


class MainWindow(QMainWindow, Main):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.add_password.clicked.connect(self.addPassword)
        self.about_program.triggered.connect(self.aboutProgram)

    def addPassword(self):
        addPasswordDialog = AddPassword(self)
        addPasswordDialog.exec_()

    def aboutProgram(self):
        aboutProgram = AboutProgram(self)
        aboutProgram.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("res/icons/icon2"))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
