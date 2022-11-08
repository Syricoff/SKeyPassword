import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QLineEdit

from DataBase import DataBase
from dialogs import AddPassword, AboutProgram
from src.res.ui.ui_MainWindow import Ui_MainWindow
from src.res.ui.ui_PasswordView import Ui_PasswordView


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.password_boxes: list[PasswordViewBox] = []
        # Подгружаем базу данных, список категорий и паролей
        self.db = DataBase()
        self.load_filter_list()
        # Подключения кнопок
        self.add_password_button.clicked.connect(self.add_password)
        self.about_program_button.triggered.connect(self.about_program)
        self.filter.currentTextChanged.connect(self.load_filter_list)
        self.types_or_apps_list.itemClicked.connect(
            lambda value:
            self.show_passwords(value.text())
        )
        self.change_db_button.triggered.connect(self.change_db)
        self.search.textEdited.connect(self.searching)

    def change_db(self):
        self.db.change_db(QFileDialog.getOpenFileName(
            self, 'Выбрать базу данных', '',
            'База данных (*db), (*sqlite);;Все файлы (*)')[0]
                          )
        self.load_filter_list()

    def load_filter_list(self):
        """Выводит список категорий"""
        # Вывод списка всех паролей
        self.show_passwords()
        # Очистка списка категорий / приложений
        self.types_or_apps_list.clear()
        # В зависимости от выбранного фильтра
        # выводится список приложений или список категорий
        if self.filter.currentText() == "Категории":
            self.types_or_apps_list.addItems(self.db.get_categories())
        elif self.filter.currentText() == "Приложения":
            self.types_or_apps_list.addItems(self.db.get_apps())

    def add_password(self):
        """Вызывает диалог добавления пароля"""
        add_password_dialog = AddPassword(self)
        add_password_dialog.exec_()
        # Обновляем фильтр на случай, если добавляли категории или приложения
        self.load_filter_list()

    def about_program(self):
        """Вызывет диалог 'О программе' """
        about_program_dialog = AboutProgram(self)
        about_program_dialog.exec_()

    def show_passwords(self, item=''):
        """Выводит список паролей в виде объектов класса PasswordViewBox"""
        # Создаём виджет и layout которые в дальнейшем положим в scrollArea
        widget = QWidget()
        vbox = QVBoxLayout()
        widget.setLayout(vbox)
        # Очищаем список экземпляров PasswordViewBox
        self.password_boxes.clear()
        # В цикле заполняем layout и список экземплярами PasswordViewBox
        for id in self.db.load_id(self.filter.currentText(), item):
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
        # Подключаем базу данных
        self.db = DataBase()
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
        # Подключения кнопок
        self.eye.toggled.connect(self.show_password)
        self.copy.clicked.connect(self.copy_password)
        self.erase.clicked.connect(self.erase_password)
        self.edit.toggled.connect(self.edit_password)
        self.save.clicked.connect(self.save_changes)

    def load_apps_and_types(self):
        """Подгружает и выводит списки приложений и категорий"""
        self.app_edit.clear()
        self.category_edit.clear()
        self.app_edit.addItems(self.db.get_apps())
        self.category_edit.addItems(self.db.get_categories())

    def load_data(self):
        # По id получаем все поля
        login, password, app, category = self.db.get_entry(self.id)
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
        self.load_data()
        self.password.setClearButtonEnabled(flag)
        self.password.setReadOnly(not flag)
        if flag:
            self.setTitle("Редактирование")

    def erase_password(self):
        answ = QMessageBox.question(self,
                                    'Подтвердждение действия',
                                    f"Действительно хотите удалить запись?\n"
                                    f"Категория: {self.category.text()}\n"
                                    f"Приложение: {self.title()}\n"
                                    f"Логин: {self.login.text()}",
                                    QMessageBox.Yes, QMessageBox.No)
        if answ == QMessageBox.Yes:
            self.db.delete(self.id)
            self.deleteLater()
            self.main.load_filter_list()

    def save_changes(self):
        # Довольно странная проверка на наличие такой же записи в базе
        #
        if ((self.db.get_id(self.get_items()) is None) or
                (self.db.get_id(self.get_items()) == (self.id,))):
            self.db.overwrite(self.id, self.get_items())
            self.main.load_filter_list()
        else:
            answ = QMessageBox.question(self,
                                        'Подтвердждение действия',
                                        "Запись с такими данными "
                                        "уже существует!\n"
                                        "\tЖелаете перезаписать?",
                                        QMessageBox.Yes, QMessageBox.No
                                        )
            if answ == QMessageBox.Yes:
                self.db.delete(self.db.get_id(self.get_items()))
                self.db.overwrite(self.id, self.get_items())
                self.main.load_filter_list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("res/icons/icon2"))  # Иконка приложения
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
