from ui.ui_Add_password import Ui_Add_password
from ui.ui_AboutApp import Ui_AboutApp
from PyQt5.QtWidgets import QDialog


class AddPassword(QDialog, Ui_Add_password):
    def __init__(self, mainWindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def addTOdb(self):
        pass

    def accept(self) -> None:

        return super().accept()

    def reject(self) -> None:
        return super().reject()


class AboutProgram(QDialog, Ui_AboutApp):
    def __init__(self, mainWindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.rejected.connect(self.reject)

    def reject(self) -> None:
        return super().reject()
