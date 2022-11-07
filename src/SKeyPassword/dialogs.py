from PyQt5.QtWidgets import QDialog, QPushButton, QDialogButtonBox

from DataBase import DataBase
from errors import (PasswordError, LoginError, AppError,
                    CategoryError, DataExistError)

from ui.ui_Add_password import Ui_Add_password
from ui.ui_AboutApp import Ui_AboutApp


class AddPassword(QDialog, Ui_Add_password):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setupUi(self)
        # Добавляем кнопки сохранить и заменить в buttonBox
        self.save_button = QPushButton("Сохранить")
        self.overwrite_button = QPushButton("Перезаписать")
        self.buttonBox.addButton(self.save_button,
                                 QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.overwrite_button,
                                 QDialogButtonBox.ActionRole)
        # Прячем label для вывода ошибок и кнопку перезаписи
        self.errors.hide()
        self.overwrite_button.hide()
        # Подгружаем базу данных и списоки категорий и приложений
        self.db = DataBase()
        self.loadAppsAndCategories()
        # Подключения кнопок
        self.save_button.clicked.connect(self.save)
        self.overwrite_button.clicked.connect(self.overwrite)
        self.category.currentTextChanged.connect(self.overwrite_button.hide)
        self.app.currentTextChanged.connect(self.overwrite_button.hide)
        self.login.textChanged.connect(self.overwrite_button.hide)

    def getItems(self) -> tuple[str, str, str, str]:
        return tuple(map(lambda x: x.strip(),
                         (self.category.currentText(),
                          self.app.currentText(),
                          self.login.text(),
                          self.password.text())))

    def loadAppsAndCategories(self):
        """Подгружает и выводит списки приложений и категорий"""
        self.app.addItems(self.db.getApps())
        self.category.addItems(self.db.getCategories())

    def validator(self):
        category, app, login, password = self.getItems()
        if not app:
            raise AppError("Поле Приложение не может быть пустым")
        if not login:
            raise LoginError("Поле Логин не может быть пустым")
        if not category:
            raise CategoryError("Поле Категория не может быть пустым")
        if not password:
            raise PasswordError("Поле Пароль не может быть пустым")

    def addEntry(self) -> bool | None:
        """Добавляет полученные данные в базу данных"""
        try:
            self.validator()  # Проверка на пустые поля
            if self.db.getId(self.getItems()) is not None:
                raise DataExistError("Запись уже существует")
            self.db.add(self.getItems())
            self.success("Успешно сохранено")
            return True
        except DataExistError as e:
            self.error(e)
            self.overwrite_button.show()
        except ValueError as e:
            self.error(e)

    def save(self) -> None:
        if self.addEntry():
            return self.accept()

    def error(self, error):
        self.errors.show()
        self.errors.setStyleSheet("color: red")
        self.errors.setText(f"{error}")

    def success(self, text):
        self.errors.show()
        self.errors.setStyleSheet("color: green")
        self.errors.setText(text)

    def overwrite(self):
        self.db.overwrite(self.db.getId(self.getItems())[0],
                          self.getItems())
        self.overwrite_button.hide()
        self.success('Успешно перезаписано')


class AboutProgram(QDialog, Ui_AboutApp):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.rejected.connect(self.reject)

    def reject(self) -> None:
        return super().reject()
