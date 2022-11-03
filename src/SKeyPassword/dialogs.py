from ui.ui_Add_password import Ui_Add_password
from ui.ui_AboutApp import Ui_AboutApp
from PyQt5.QtWidgets import QDialog
import sqlite3


class AddPassword(QDialog, Ui_Add_password):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setupUi(self)
        # Подгружаем базу данных и списоки категорий и приложений
        self.con = sqlite3.connect("res/passwords.sqlite")
        self.loadAppsAndTypes(main_window)
        # Подключения кнопок
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.reject)

    def add_type_if(self):
        """Проверяет есть ли категория в базе данных
                        и если нет, добавляет её туда"""
        cur = self.con.cursor()
        result = cur.execute('''
                             SELECT * FROM types
                             WHERE type_name = ?
                             ''', (self.type.currentText(), ))
        if not result.fetchone():
            cur.execute('''
                        INSERT INTO Types(type_name)
                        VALUES(?)
                        ''', (self.type.currentText(), ))
            self.con.commit()

    def add_to_db(self):
        """Добавляет полученные данные в базу данных"""
        self.add_type_if()  # Отдельно проверим наличие категории
        cur = self.con.cursor()
        cur.execute("""
                    INSERT INTO Passwords(app_name, login, password, app_type)
                    VALUES(?, ?, ?, (SELECT id FROM Types WHERE type_name = ?))
                    """, (self.app.currentText(), self.login.text(),
                          self.password.text(), self.type.currentText()))
        self.con.commit()

    def loadAppsAndTypes(self, main):
        """Подгружает и выводит списки приложений и категорий"""
        self.app.addItems(main.loadApps())
        self.type.addItems(main.loadTypes())

    def save(self) -> None:
        """Кнопка 'сохранить' """
        self.add_to_db()
        return super().accept()

    def reject(self) -> None:
        """Кнопка 'отмена' """
        return super().reject()


class AboutProgram(QDialog, Ui_AboutApp):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.rejected.connect(self.reject)

    def reject(self):
        return super().reject()
