from PyQt5.QtWidgets import QDialog, QPushButton, QDialogButtonBox

from DataBase import DataBase
from Errors import (PasswordError, LoginError, AppError,
                    CategoryError, DataExistError)

from res.ui.ui_AddPassword import Ui_Add_password
from res.ui.ui_AboutApp import Ui_AboutApp

db = DataBase()


class AddPassword(QDialog, Ui_Add_password):
    def __init__(self, main):
        QDialog.__init__(self)
        self.setupUi(self)
        self.main = main
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
        # Подгружаем списки категорий и приложений
        self.load_apps_and_categories()
        # Подключения кнопок
        self.save_button.clicked.connect(self.save)
        self.overwrite_button.clicked.connect(self.overwrite)
        self.category.currentTextChanged.connect(self.overwrite_button.hide)
        self.app.currentTextChanged.connect(self.overwrite_button.hide)
        self.login.textChanged.connect(self.overwrite_button.hide)

    def get_items(self) -> tuple:
        return tuple(map(lambda x: x.strip(),
                         (self.category.currentText(),
                          self.app.currentText(),
                          self.login.text(),
                          self.password.text())))

    def load_apps_and_categories(self):
        """Подгружает и выводит списки приложений и категорий"""
        self.app.addItems(db.get_apps())
        self.category.addItems(db.get_categories())

    def validator(self):
        category, app, login, password = self.get_items()
        if not app:
            raise AppError("Поле Приложение не может быть пустым")
        if not login:
            raise LoginError("Поле Логин не может быть пустым")
        if not category:
            raise CategoryError("Поле Категория не может быть пустым")
        if not password:
            raise PasswordError("Поле Пароль не может быть пустым")

    def add_entry(self) -> bool | None:
        """Добавляет полученные данные в базу данных"""
        try:
            self.validator()  # Проверка на пустые поля
            if db.get_id(self.get_items()) is not None:
                raise DataExistError("Запись уже существует")
            db.add(self.get_items())
            self.success("Успешно сохранено")
            return True
        except DataExistError as e:
            self.error(e)
            self.overwrite_button.show()
        except ValueError as e:
            self.error(e)

    def save(self) -> None:
        if self.add_entry():
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
        db.overwrite(db.get_id(self.get_items()), self.get_items())
        self.overwrite_button.hide()
        self.success('Успешно перезаписано')


class AboutProgram(QDialog, Ui_AboutApp):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.rejected.connect(self.reject)

    def reject(self) -> None:
        return super().reject()
