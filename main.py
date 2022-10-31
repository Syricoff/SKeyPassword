import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
import sqlite3

from dialogs import AddPassword, AboutProgram
from ui.ui_MainWindow import Ui_MainWindow as Main


class MainWindow(QMainWindow, Main):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # Подгружаем базу данных и список категорий
        self.con = sqlite3.connect("res/passwords.sqlite")
        self.loadListTypes()
        # Подключения кнопок
        self.add_password.clicked.connect(self.addPassword)
        self.about_program.triggered.connect(self.aboutProgram)
        # self.pushButton.clicked.connect(self.run)

    def loadListTypes(self):
        """Выводит список категорий"""
        self.types_list.clear()
        self.types_list.addItems(self.loadTypes())

    def addPassword(self):
        """Вызывает диалог добавления пароля"""
        addPasswordDialog = AddPassword(self)
        addPasswordDialog.exec()
        self.loadListTypes()

    def aboutProgram(self):
        """Вызывет диалог 'О программе' """
        aboutProgram = AboutProgram(self)
        aboutProgram.exec()

    def loadApps(self) -> list[str]:
        """Загружает и возвращает список приложений"""
        cur = self.con.cursor()
        return list(map(lambda x: x[0], cur.execute('''
                    SELECT DISTINCT app_name FROM Passwords
                    ''').fetchall()))

    def loadTypes(self) -> list[str]:
        """Загружает и возвращает список категорий"""
        cur = self.con.cursor()
        return list(map(lambda x: x[0], cur.execute('''
                    SELECT type_name
                    FROM Types
                    WHERE id IN
                    (SELECT app_type FROM Passwords)
                    ''').fetchall()))

    # def run(self):
    #     cur = self.con.cursor()
    #     print(cur.execute("""
    #                 SELECT * From Passwords""").fetchall())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("res/icons/icon2"))  # Иконка приложения
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
