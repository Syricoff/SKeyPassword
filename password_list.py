from PyQt5.QtWidgets import (QApplication, QGroupBox, QLineEdit,
                             QGridLayout, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon


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
