import sys
import sqlite3


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import (QVBoxLayout, QGroupBox, QLineEdit,
                             QGridLayout, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon

from dialogs import AddPassword, AboutProgram
from ui.ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
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


class PasswordView(QGroupBox):
    def __init__(self, login, password):
        super().__init__()
        self.setTitle(login)
        # Подгружаю иконки
        eye_icon = QIcon()
        eye_icon.addPixmap(QPixmap("./res/icons/eye-outline.svg"),
                           QIcon.Normal, QIcon.Off)
        eye_icon.addPixmap(QPixmap("./res/icons/eye-off-outline.svg"),
                           QIcon.Normal, QIcon.On)
        copy_icon = QIcon()
        copy_icon.addPixmap(QPixmap("./res/icons/content-copy.svg"),
                            QIcon.Normal, QIcon.Off)
        # Создаю lineEdit для пароля
        self.lineEdit = QLineEdit(password)
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.lineEdit.setReadOnly(True)
        # Создаю кнопку для переключения видимости пароля
        self.eye = QPushButton()
        self.eye.setCheckable(True)
        self.eye.setIcon(eye_icon)
        # Кнопка для быстрого копирования пароля в буфер
        self.copy = QPushButton()
        self.copy.setIcon(copy_icon)
        # Создание layout и добавление в него элементов
        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.eye, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.copy, 0, 2, 1, 1)
        # Подключения кнопок
        self.eye.toggled.connect(self.showpassword)
        self.copy.clicked.connect(self.copy_password)

    def showpassword(self, flag):
        """Если кнопка нажата то переводит lineEdit
                в обычный режим, иначе в режим пароля"""
        if flag:
            self.lineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.lineEdit.setEchoMode(QLineEdit.Password)

    def copy_password(self):
        """Добавляет пароль в буфер обмена"""
        QApplication.clipboard().setText(self.lineEdit.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("res/icons/icon2"))  # Иконка приложения
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
