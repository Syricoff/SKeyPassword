from ui.ui_Add_password import Ui_Add_password
from ui.ui_AboutApp import Ui_AboutApp
from errors import *

from PyQt5.QtWidgets import QDialog, QPushButton, QDialogButtonBox
import sqlite3


class AddPassword(QDialog, Ui_Add_password):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setupUi(self)
        self.errors.hide()
        self.save_button = QPushButton("Сохранить")
        self.buttonBox.addButton(self.save_button, QDialogButtonBox.ActionRole)
        # Подгружаем базу данных и списоки категорий и приложений
        self.con = sqlite3.connect("res/passwords.sqlite")
        self.loadAppsAndTypes(main_window)
        # Подключения кнопок
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.save_button.clicked.connect(self.save)

    def add_category_if(self):
        """Проверяет есть ли категория в базе данных
                        и если нет, добавляет её туда"""
        cur = self.con.cursor()
        result = cur.execute('''
                             SELECT * FROM types
                             WHERE type_name = ?
                             ''', (self.category.currentText(), ))
        if not result.fetchone():
            cur.execute('''
                        INSERT INTO Types(type_name)
                        VALUES(?)
                        ''', (self.category.currentText(), ))
            self.con.commit()
            
    def validator(self):
        category = self.category.currentText()
        app = self.app.currentText()
        login = self.login.text()
        password = self.password.text()
        if not app.strip():
            raise AppError("Приложение")
        if not login.strip():
            raise LoginError("Логин")
        if not category.strip():
            raise CategoryError("Категория")
        if not password.strip():
            raise PasswordError("Пароль")
        
    def add_to_db(self):
        """Добавляет полученные данные в базу данных"""
        try:
            self.validator()
            self.add_category_if()  # Отдельно проверим наличие категории
            cur = self.con.cursor()
            cur.execute("""
                        INSERT INTO
                        Passwords(app_name, login, password, app_type)
                        VALUES(?, ?, ?,
                        (SELECT id FROM Types WHERE type_name = ?))
                        """, (self.app.currentText(), self.login.text(),
                            self.password.text(), self.category.currentText()))
            self.con.commit()
            self.errors.hide()
        except ValueError as e:
            self.errors.show()
            self.errors.setText(f"Поле {e} не может быть пустым")
            

    def loadAppsAndTypes(self, main):
        """Подгружает и выводит списки приложений и категорий"""
        self.app.addItems(main.loadApps())
        self.category.addItems(main.loadTypes())

    def accept(self) -> None:
        """Кнопка 'ок' """
        return super().accept()

    def reject(self) -> None:
        """Кнопка 'отмена' """
        return super().reject()
    
    def save(self) -> None:
        self.add_to_db()


class AboutProgram(QDialog, Ui_AboutApp):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.rejected.connect(self.reject)

    def reject(self):
        return super().reject()

