import sys
import sqlite3


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import (QVBoxLayout, QGroupBox, QLineEdit,
                             QLabel, QHBoxLayout, QGridLayout,
                             QPushButton, QSizePolicy)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore

from dialogs import AddPassword, AboutProgram
from ui.ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.password_boxes: list[PasswordViewBox] = []
        # Подгружаем базу данных, список категорий и паролей
        self.con = sqlite3.connect("res/passwords.sqlite")
        self.loadFilterList()
        self.showLoginAndPasswords(every=True)
        # Подключения кнопок
        self.add_password.clicked.connect(self.addPassword)
        self.about_program.triggered.connect(self.aboutProgram)
        self.filter.currentTextChanged.connect(self.loadFilterList)
        self.types_or_apps_list.itemClicked.connect(
                                    lambda value:
                                    self.showLoginAndPasswords(value.text())
                                                    )
        self.search.textEdited.connect(self.searching)

    def loadFilterList(self):
        """Выводит список категорий"""
        # Очистка списка категорий / приложений
        self.types_or_apps_list.clear()
        # Вывод списка всех паролей
        self.showLoginAndPasswords(every=True)
        # Pattern matching из Python 3.10
        match self.filter.currentText():
            case "Категории":
                self.types_or_apps_list.addItems(self.loadTypes())
            case "Приложения":
                self.types_or_apps_list.addItems(self.loadApps())

    def addPassword(self):
        """Вызывает диалог добавления пароля"""
        addPasswordDialog = AddPassword(self)
        addPasswordDialog.exec_()
        # Обновляем фильтр на случай, если добавляли категории или приложения
        self.loadFilterList()

    def aboutProgram(self):
        """Вызывет диалог 'О программе' """
        aboutProgram = AboutProgram(self)
        aboutProgram.exec_()

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

    def loadLoginPassword(self, condition, every) -> list[int]:
        """Загружает и возвращает список id записей"""
        text = self.filter.currentText()
        cur = self.con.cursor()
        if every:
            return list(map(lambda x: int(x[0]),
                        cur.execute('''
                        SELECT id
                        FROM Passwords
                        ''').fetchall()))
        elif text == "Категории":
            return list(map(lambda x: int(x[0]),
                        cur.execute('''
                        SELECT id
                        FROM Passwords
                        WHERE app_type =
                        (SELECT id FROM Types
                        WHERE type_name = ?)
                        ''', (condition, )).fetchall()))
        elif text == "Приложения":
            return list(map(lambda x: int(x[0]),
                        cur.execute('''
                        SELECT id
                        FROM Passwords
                        WHERE app_name = ?
                        ''', (condition, )).fetchall()))

    def showLoginAndPasswords(self, item='', every=False):
        """Выводит список паролей в виде объектов класса PasswordViewBox"""
        # Создаём виджет и layout которые в дальнейшем положим в scrollArea
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.widget.setLayout(self.vbox)
        # Очищаем список экземпляров PasswordViewBox
        self.password_boxes.clear()
        # В цикле заполняем layout и список экземплярами PasswordViewBox
        for id in self.loadLoginPassword(item, every):
            box = PasswordViewBox(id)
            self.vbox.addWidget(box)
            self.password_boxes.append(box)
        # Загружаем виджет в scrollArea
        self.scrollArea.setWidget(self.widget)
        # Фильтруем по запросу в поиске
        self.searching(self.search.text())

    def searching(self, value):
        """Отвечает за работу виджета поиска"""
        if value := value.strip().lower():
            #  Поиск по всем элементам(логин, название приложения, категория)
            for box in self.password_boxes:
                if any(map(lambda x: x.startswith(value), box.getItems())):
                    box.show()
                else:
                    box.hide()
        else:
            for box in self.password_boxes:
                box.show()


class PasswordViewBox(QGroupBox):
    def __init__(self, id):
        super().__init__()
        # Подгружаю иконки
        eye_icon = QIcon()
        eye_icon.addPixmap(QPixmap("./res/icons/eye-outline.svg"),
                           QIcon.Normal, QIcon.Off)
        eye_icon.addPixmap(QPixmap("./res/icons/eye-off-outline.svg"),
                           QIcon.Normal, QIcon.On)
        copy_icon = QIcon()
        copy_icon.addPixmap(QPixmap("./res/icons/content-copy.svg"),
                            QIcon.Normal, QIcon.Off)
        # Подключаем базу данных
        self.con = sqlite3.connect("res/passwords.sqlite")
        cur = self.con.cursor()
        # По id получаем все поля
        login, password, app, category = cur.execute("""
                                                     SELECT
                                                     login, password,
                                                     app_name,
                                                     (SELECT type_name
                                                     FROM Types
                                                     WHERE app_type = id)
                                                     FROM Passwords
                                                     WHERE id = ?
                                                     """, (id, )).fetchone()
        # Задаём название GroupBox и некоторые его параметры
        self.setTitle(app)
        self.setSizePolicy(QSizePolicy.Preferred,
                           QSizePolicy.Fixed)
        # Создание label для названия приложения и категории
        self.login = QLabel(login)
        self.login.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.category = QLabel(category)
        self.category.setAlignment(
                                QtCore.Qt.AlignRight |
                                QtCore.Qt.AlignTrailing |
                                QtCore.Qt.AlignVCenter)
        # Создаю lineEdit для пароля
        self.password = QLineEdit(password)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setReadOnly(True)
        # Создаю кнопку для переключения видимости пароля
        self.eye = QPushButton()
        self.eye.setCheckable(True)
        self.eye.setIcon(eye_icon)
        # Кнопка для быстрого копирования пароля в буфер
        self.copy = QPushButton()
        self.copy.setIcon(copy_icon)
        # Создание layout и добавление в него элементов
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.login)
        self.hLayout.addWidget(self.category)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.addLayout(self.hLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.password, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.eye, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.copy, 1, 2, 1, 1)
        # Подключения кнопок
        self.eye.toggled.connect(self.show_password)
        self.copy.clicked.connect(self.copy_password)

    def getItems(self) -> tuple[str, str, str]:
        return tuple(map(str.lower,
                         (self.login.text(),
                          self.title(),
                          self.category.text())))

    def show_password(self, flag):
        """Если кнопка нажата то переводит password
                в обычный режим, иначе в режим пароля"""
        if flag:
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def copy_password(self):
        """Добавляет пароль в буфер обмена"""
        QApplication.clipboard().setText(self.password.text())

    def edit_password(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("res/icons/icon2"))  # Иконка приложения
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
