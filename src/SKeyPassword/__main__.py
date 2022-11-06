import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QLineEdit
from PyQt5.QtGui import QIcon

from DataBase import DataBase
from dialogs import AddPassword, AboutProgram
from ui.ui_MainWindow import Ui_MainWindow
from ui.ui_PasswordView import Ui_PasswordView


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.password_boxes: list[PasswordViewBox] = []
        # Подгружаем базу данных, список категорий и паролей
        self.db = DataBase()
        self.loadFilterList()
        self.showLoginAndPasswords()
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
        self.showLoginAndPasswords()
        # Pattern matching из Python 3.10
        match self.filter.currentText():
            case "Категории":
                self.types_or_apps_list.addItems(self.db.getCategories())
            case "Приложения":
                self.types_or_apps_list.addItems(self.db.getApps())

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

    def showLoginAndPasswords(self, item=''):
        """Выводит список паролей в виде объектов класса PasswordViewBox"""
        # Создаём виджет и layout которые в дальнейшем положим в scrollArea
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.widget.setLayout(self.vbox)
        # Очищаем список экземпляров PasswordViewBox
        self.password_boxes.clear()
        # В цикле заполняем layout и список экземплярами PasswordViewBox
        for id in self.db.loadId(self.filter.currentText(), item):
            box = PasswordViewBox(id, self)
            self.vbox.addWidget(box)
            self.password_boxes.append(box)
        # Загружаем виджет в scrollArea
        self.scrollArea.setWidget(self.widget)
        # Фильтруем по запросу в поиске
        self.searching(self.search.text())

    def searching(self, value):
        """Отвечает за работу виджета поиска"""
        if value := value.strip().title():
            #  Поиск по всем элементам(логин, название приложения, категория)
            for box in self.password_boxes:
                if any(map(lambda x: x.startswith(value), box.getItems()[:3])):
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
        # Подключаем базу данных
        self.db = DataBase()
        self.loadData()
        self.loadAppsAndTypes()
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
        self.eye.toggled.connect(self.showPassword)
        self.copy.clicked.connect(self.copyPassword)
        self.erase.clicked.connect(self.erasePassword)
        self.edit.toggled.connect(self.editPassword)
        self.save.clicked.connect(self.saveChanges)

    def loadAppsAndTypes(self):
        """Подгружает и выводит списки приложений и категорий"""
        self.app_edit.addItems(self.db.getApps())
        self.category_edit.addItems(self.db.getCategories())

    def loadData(self):
        # По id получаем все поля
        login, password, app, category = self.db.getEntry(self.id)
        # Выводим информацию
        self.setTitle(app)
        self.category.setText(category)
        self.login.setText(login)
        self.password.setText(password)
        # В неактивные тоже
        self.login_edit.setText(login)
        self.app_edit.setCurrentIndex(
                            self.app_edit.findText(app))
        self.category_edit.setCurrentIndex(
                            self.category_edit.findText(category))

    def getItems(self) -> tuple[str, str, str, str]:
        return tuple(map(str.title,
                         (self.category_edit.currentText(),
                          self.app_edit.currentText(),
                          self.login_edit.text(),
                          self.password.text())))

    def showPassword(self, flag):
        """Если кнопка нажата то переводит password
                в обычный режим, иначе в режим пароля"""
        if flag:
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def copyPassword(self):
        """Добавляет пароль в буфер обмена"""
        QApplication.clipboard().setText(self.password.text())

    def editPassword(self, flag):
        self.loadData()
        self.password.setClearButtonEnabled(flag)
        self.password.setReadOnly(not flag)
        if flag:
            self.setTitle("Редактирование")

    def erasePassword(self):
        answ = QMessageBox.question(self,
                                    'Подтвердждение действия',
                                    f"Действительно удалить хотите \
                                    удалить эту запись?\n \
                                    Категория: {self.category.text()}\n \
                                    Приложение: {self.title()}\n \
                                    Логин: {self.login.text()}",
                                    QMessageBox.Yes, QMessageBox.No)
        if answ == QMessageBox.Yes:
            self.db.delete(self.id)
            self.deleteLater()

    def saveChanges(self):
        if len(self.db.loadId(condition="id", args=self.getItems())) <= 1:
            self.db.overwrite(self.id, self.getItems())
        else:
            print('ps')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("res/icons/icon2"))  # Иконка приложения
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
