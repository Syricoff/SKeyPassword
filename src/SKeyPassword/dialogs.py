from ui.ui_Add_password import Ui_Add_password
from ui.ui_AboutApp import Ui_AboutApp
from errors import (PasswordError, LoginError, AppError,
                    CategoryError, DataExistError)

from PyQt5.QtWidgets import QDialog, QPushButton, QDialogButtonBox
import sqlite3


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
        self.con = sqlite3.connect("res/passwords.sqlite")
        self.loadAppsAndTypes(main_window)
        # Подключения кнопок
        self.save_button.clicked.connect(self.save)
        self.overwrite_button.clicked.connect(self.overwrite)
        self.category.currentTextChanged.connect(self.overwrite_button.hide)
        self.app.currentTextChanged.connect(self.overwrite_button.hide)
        self.login.textChanged.connect(self.overwrite_button.hide)

    def getItems(self) -> tuple[str, str, str, str]:
        return tuple(map(lambda x: x.strip().title(),
                         (self.category.currentText(),
                          self.app.currentText(),
                          self.login.text(),
                          self.password.text())))

    def loadAppsAndTypes(self, main):
        """Подгружает и выводит списки приложений и категорий"""
        self.app.addItems(main.loadApps())
        self.category.addItems(main.loadTypes())

    def add_category_if(self):
        """Проверяет есть ли категория в базе данных
                        и если нет, добавляет её туда"""
        cur = self.con.cursor()
        result = cur.execute('''
                             SELECT * FROM types
                             WHERE type_name = ?
                             ''', (self.category.currentText().title(), ))
        if not result.fetchone():
            cur.execute('''
                        INSERT INTO Types(type_name)
                        VALUES(?)
                        ''', (self.category.currentText().title(), ))
            self.con.commit()

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

    def is_entry_in_db(self):
        cur = self.con.cursor()
        return cur.execute("""
                            SELECT id
                            FROM Passwords
                            WHERE  app_type =
                            (SELECT id FROM Types
                            WHERE type_name = ?)
                            AND app_name = ?
                            AND login = ?
                            """, self.getItems()[:3])

    def add_to_db(self) -> bool | None:
        """Добавляет полученные данные в базу данных"""
        try:
            self.validator()  # Проверка на пустые поля
            self.add_category_if()  # Проверка наличия категории
            if self.is_entry_in_db().fetchone() is not None:
                raise DataExistError("Запись уже существует")
            cur = self.con.cursor()
            cur.execute("""
                        INSERT INTO
                        Passwords(app_type, app_name, login, password)
                        VALUES((SELECT id FROM Types WHERE
                        type_name = ?), ?, ?, ?)
                        """, self.getItems())
            self.con.commit()
            self.success("Успешно сохранено")
            return True
        except DataExistError as e:
            self.error(e)
            self.overwrite_button.show()
        except ValueError as e:
            self.error(e)

    def save(self) -> None:
        if self.add_to_db():
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
        cur = self.con.cursor()
        id, = self.is_entry_in_db().fetchone()
        cur.execute("""
                    UPDATE Passwords
                    SET app_type =
                    (SELECT id FROM Types
                    WHERE type_name = ?),
                    app_name = ?,
                    login = ?,
                    password = ?
                    WHERE id = ?
                    """, self.getItems() + (id,))
        self.con.commit()
        self.overwrite_button.hide()
        self.success('Успешно перезаписано')


class AboutProgram(QDialog, Ui_AboutApp):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.rejected.connect(self.reject)

    def reject(self) -> None:
        return super().reject()
