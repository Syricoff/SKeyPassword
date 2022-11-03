# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/syricoff/PycharmProjects/SKeyPassword/src/SKeyPassword/ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon_search = QtWidgets.QLabel(self.centralwidget)
        self.icon_search.setStyleSheet("color: white")
        self.icon_search.setText("")
        self.icon_search.setPixmap(QtGui.QPixmap("./res/icons/search_icon.svg"))
        self.icon_search.setScaledContents(False)
        self.icon_search.setOpenExternalLinks(False)
        self.icon_search.setObjectName("icon_search")
        self.horizontalLayout.addWidget(self.icon_search)
        self.search = QtWidgets.QLineEdit(self.centralwidget)
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 414, 291))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.add_password = QtWidgets.QPushButton(self.centralwidget)
        self.add_password.setAcceptDrops(False)
        self.add_password.setFlat(False)
        self.add_password.setObjectName("add_password")
        self.gridLayout.addWidget(self.add_password, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./res/icons/filter.svg"))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.filter = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter.sizePolicy().hasHeightForWidth())
        self.filter.setSizePolicy(sizePolicy)
        self.filter.setStyleSheet("text-align: center")
        self.filter.setEditable(False)
        self.filter.setObjectName("filter")
        self.filter.addItem("")
        self.filter.addItem("")
        self.horizontalLayout_2.addWidget(self.filter)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.types_or_apps_list = QtWidgets.QListWidget(self.centralwidget)
        self.types_or_apps_list.setObjectName("types_or_apps_list")
        self.verticalLayout.addWidget(self.types_or_apps_list)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 29))
        self.menubar.setObjectName("menubar")
        self.Menu = QtWidgets.QMenu(self.menubar)
        self.Menu.setObjectName("Menu")
        self.help = QtWidgets.QMenu(self.menubar)
        self.help.setObjectName("help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("font color: red")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.about_program = QtWidgets.QAction(MainWindow)
        self.about_program.setObjectName("about_program")
        self.actiondsdsv = QtWidgets.QAction(MainWindow)
        self.actiondsdsv.setObjectName("actiondsdsv")
        self.help.addAction(self.about_program)
        self.menubar.addAction(self.Menu.menuAction())
        self.menubar.addAction(self.help.menuAction())

        self.retranslateUi(MainWindow)
        self.filter.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SKeyPassword"))
        self.search.setPlaceholderText(_translate("MainWindow", "Поиск"))
        self.add_password.setText(_translate("MainWindow", "Добавить пароль"))
        self.filter.setItemText(0, _translate("MainWindow", "Категории"))
        self.filter.setItemText(1, _translate("MainWindow", "Приложения"))
        self.Menu.setTitle(_translate("MainWindow", "Меню"))
        self.help.setTitle(_translate("MainWindow", "Справка"))
        self.about_program.setText(_translate("MainWindow", "О приложении"))
        self.actiondsdsv.setText(_translate("MainWindow", "dsdsv"))
