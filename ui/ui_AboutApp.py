# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/syricoff/PycharmProjects/SKeyPassword/ui/AboutApp.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutApp(object):
    def setupUi(self, AboutApp):
        AboutApp.setObjectName("AboutApp")
        AboutApp.resize(477, 574)
        self.gridLayout = QtWidgets.QGridLayout(AboutApp)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutApp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(AboutApp)
        self.label_2.setText("")
        self.label_2.setTextFormat(QtCore.Qt.MarkdownText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(AboutApp)
        self.label_3.setTextFormat(QtCore.Qt.MarkdownText)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AboutApp)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./res/icons/icon2.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.retranslateUi(AboutApp)
        QtCore.QMetaObject.connectSlotsByName(AboutApp)

    def retranslateUi(self, AboutApp):
        _translate = QtCore.QCoreApplication.translate
        AboutApp.setWindowTitle(_translate("AboutApp", "О Приложении"))
        self.label_3.setText(_translate("AboutApp", "SKeyPassword - кросспалтформенный менеджер паролей, написанный на Python с использованием Qt5"))
