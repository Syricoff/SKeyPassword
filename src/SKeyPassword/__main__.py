import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QLineEdit

from DataBase import DataBase
from dialogs import AddPassword, AboutProgram
from res.ui.ui_MainWindow import Ui_MainWindow
from res.ui.ui_PasswordView import Ui_PasswordView
from res.icons import rc_res


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # Список, в котором будут храниться пароли
        self.password_boxes: list[PasswordViewBox] = []
        # Подгружаем список приложений
        self.load_data()
        # Подключения кнопок
        self.add_password_button.clicked.connect(self.add_password)
        self.about_program_button.triggered.connect(self.about_program)
        self.category.activated.connect(self.load_data)
        self.apps_list.itemClicked.connect(
            lambda value:
            self.show_passwords(value.text())
        )
        self.change_db_button.triggered.connect(self.change_db)
        self.search.textEdited.connect(self.searching)

    def change_db(self):
        """File dialog для выбора файла базы данных"""
        db.change_db(QFileDialog.getOpenFileName(
            self, 'Выбрать базу данных', '',
            'База данных (*db), (*sqlite);;Все файлы (*)')[0]
                          )
        self.load_data()

    def load_catigories(self):
        if len(self.category) - 1 != len(db.get_categories()):
            self.category.clear()
            self.category.addItem("Все приложения")
            self.category.addItems(db.get_categories())

    def load_data(self):
        """Выводит все данные из базы данных в нужные виджеты"""
        # Загрузка списка категорий
        self.load_catigories()
        # Вывод списка всех паролей
        self.show_passwords()
        # Очистка списка приложений
        self.apps_list.clear()
        # Вывод списка приложений
        if (category := self.category.currentText()) == "Все приложения":
            self.apps_list.addItems(db.get_apps())
        else:
            self.apps_list.addItems(db.get_apps(category))

    def add_password(self):
        """Вызывает диалог добавления пароля"""
        add_password_dialog = AddPassword(self)
        add_password_dialog.exec_()
        # Обновляем данные
        self.load_data()

    def about_program(self):
        """Вызывет диалог 'О программе' """
        about_program_dialog = AboutProgram(self)
        about_program_dialog.exec_()

    def show_passwords(self, item=None, category=None):
        """Выводит список паролей в виде объектов класса PasswordViewBox"""
        # Создаём виджет и layout которые в дальнейшем положим в scrollArea
        widget = QWidget()
        vbox = QVBoxLayout()
        widget.setLayout(vbox)
        # Очищаем список экземпляров PasswordViewBox
        self.password_boxes.clear()
        # В цикле заполняем layout и список экземплярами PasswordViewBox
        if self.category.currentText() != "Все приложения":
            category = self.category.currentText()
        for id in db.load_id(item, category):
            box = PasswordViewBox(id, self)
            vbox.addWidget(box)
            self.password_boxes.append(box)
        # Загружаем виджет в scrollArea
        self.scrollArea.setWidget(widget)
        # Фильтруем по запросу в поиске
        self.searching(self.search.text())

    def searching(self, value):
        """Отвечает за работу виджета поиска"""
        if value := value.strip().title():
            #  Поиск по всем элементам(логин, название приложения, категория)
            for box in self.password_boxes:
                if any(map(lambda x: x.startswith(value),
                           box.get_items()[:3])):
                    box.show()
                else:
                    box.hide()
        else:
            for box in self.password_boxes:
                box.show()


class PasswordViewBox(QGroupBox, Ui_PasswordView):
    def __init__(self, id, main):
        QGroupBox.__init__(self)
        self.setupUi(self)
        self.id = id
        self.main = main
        # Подгружаем данные
        self.load_data()
        # Прячем не нужные виджеты
        self.save.setVisible(False)
        self.label_category.setVisible(False)
        self.label_app.setVisible(False)
        self.login_edit.setVisible(False)
        self.label_login.setVisible(False)
        self.label_password.setVisible(False)
        self.app_edit.setVisible(False)
        self.category_edit.setVisible(False)
        # Подключаем кнопки
        self.eye.toggled.connect(self.show_password)
        self.copy.clicked.connect(self.copy_password)
        self.erase.clicked.connect(self.erase_password)
        self.edit.toggled.connect(self.edit_password)
        self.save.clicked.connect(self.save_changes)

    def load_apps_and_types(self):
        """Подгружает и выводит списки приложений и категорий"""
        self.app_edit.clear()
        self.category_edit.clear()
        self.app_edit.addItems(db.get_apps())
        self.category_edit.addItems(db.get_categories())

    def load_data(self):
        # По id получаем все поля
        category, app, login, password = db.get_entry(self.id)
        # Выводим информацию
        self.setTitle(app)
        self.category.setText(category)
        self.login.setText(login)
        self.password.setText(password)
        self.load_apps_and_types()
        # В неактивные тоже
        self.login_edit.setText(login)
        self.app_edit.setCurrentIndex(
            self.app_edit.findText(app))
        self.category_edit.setCurrentIndex(
            self.category_edit.findText(category))

    def get_items(self) -> tuple[str, str, str, str]:
        """Получание данных с виджетов"""
        return tuple(map(str.title,
                         (self.category_edit.currentText(),
                          self.app_edit.currentText(),
                          self.login_edit.text(),
                          ))) + (self.password.text(),)

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

    def edit_password(self, flag):
        """При нажатии показывает меню изменения пароля"""
        # Обновляем данные
        self.load_data()
        self.password.setClearButtonEnabled(flag)
        self.password.setReadOnly(not flag)
        if flag:
            self.setTitle("Редактирование")

    def erase_password(self):
        """Вызывает диалог удаления пароля"""
        answ = QMessageBox.question(self,
                                    'Подтвердждение действия',
                                    f"Действительно хотите удалить запись?\n"
                                    f"Категория: {self.category.text()}\n"
                                    f"Приложение: {self.title()}\n"
                                    f"Логин: {self.login.text()}",
                                    QMessageBox.Yes, QMessageBox.No)
        if answ == QMessageBox.Yes:
            db.delete(self.id)
            self.deleteLater()
            # Обновляем данные в основном окне
            self.main.load_data()

    def save_changes(self):
        """Сохраняет изменения"""
        # Проверяем есть ли запись в бд
        # Так же проверка по id в случае изменения категории
        if ((db.get_id(self.get_items()) is None) or
                (db.get_id(self.get_items()) == self.id)):
            db.overwrite(self.id, self.get_items())
            # Обновляем данные основного окна
            self.main.load_data()
        else:
            # Вызывает диалог перезаписи пароля
            answ = QMessageBox.question(self,
                                        'Подтвердждение действия',
                                        "Запись с такими данными "
                                        "уже существует!\n"
                                        "\tЖелаете перезаписать?",
                                        QMessageBox.Yes, QMessageBox.No
                                        )
            if answ == QMessageBox.Yes:
                # Удаляет другую запись с такими же данными
                db.delete(db.get_id(self.get_items()))
                # Перезаписываем данные в редактируемый box
                db.overwrite(self.id, self.get_items())
                # Обновляем данные главного окна
                self.main.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("/ res/icons/icon2.png"))  # Иконка приложения
    db = DataBase()
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
