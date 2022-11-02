import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
import sqlite3

from dialogs import AddPassword, AboutProgram
from ui.ui_MainWindow import Ui_MainWindow as Main
from password_list import PasswordView


class MainWindow(QMainWindow, Main):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # Подгружаем базу данных и список категорий
        self.con = sqlite3.connect("res/passwords.sqlite")
        self.loadFilterList()
        # Подключения кнопок
        self.add_password.clicked.connect(self.addPassword)
        self.about_program.triggered.connect(self.aboutProgram)
        self.pushButton.clicked.connect(self.run)
        self.filter.currentTextChanged.connect(self.loadFilterList)
        self.types_or_apps_list.itemClicked.connect(self.showLoginAndPasswords)

    def loadFilterList(self):
        """Выводит список категорий"""
        self.scrollArea.setWidget(QWidget())  # Очищение scrollArea
        self.types_or_apps_list.clear()
        if self.filter.currentText() == "Категории":
            self.types_or_apps_list.addItems(self.loadTypes())
        elif self.filter.currentText() == "Приложения":
            self.types_or_apps_list.addItems(self.loadApps())

    def addPassword(self):
        """Вызывает диалог добавления пароля"""
        addPasswordDialog = AddPassword(self)
        addPasswordDialog.exec()
        self.loadFilterList()

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

    def loadLoginPassword(self, condition) -> list[tuple[str, str]]:
        """Загружает и возвращает список кортежей из логина и пароля"""
        cur = self.con.cursor()
        return cur.execute('''
                    SELECT login, password FROM Passwords
                    ''').fetchall()

    def showLoginAndPasswords(self, item):
        """Выводит список паролей в виде объектов класса PasswordView"""
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.widget.setLayout(self.vbox)
        for login, password in self.loadLoginPassword(item):
            self.vbox.addWidget(PasswordView(login, password))
        self.scrollArea.setWidget(self.widget)

    def run(self):
        cur = self.con.cursor()
        print(cur.execute("""
                    SELECT * From Passwords""").fetchall())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("res/icons/icon2"))  # Иконка приложения
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
