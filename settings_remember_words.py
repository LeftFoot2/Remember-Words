# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_remember_words.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(317, 172)
        self.centralwidget = QtWidgets.QWidget(Settings)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.alphabet_toggle = QtWidgets.QCheckBox(self.centralwidget)
        self.alphabet_toggle.setObjectName("alphabet_toggle")
        self.verticalLayout.addWidget(self.alphabet_toggle)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.font_change = QtWidgets.QComboBox(self.centralwidget)
        self.font_change.setMinimumSize(QtCore.QSize(234, 0))
        self.font_change.setMaximumSize(QtCore.QSize(234, 16777215))
        self.font_change.setObjectName("font_change")
        self.horizontalLayout_4.addWidget(self.font_change)
        self.font_size = QtWidgets.QSpinBox(self.centralwidget)
        self.font_size.setMaximumSize(QtCore.QSize(50, 16777215))
        self.font_size.setMinimum(5)
        self.font_size.setMaximum(17)
        self.font_size.setObjectName("font_size")
        self.horizontalLayout_4.addWidget(self.font_size)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.default_changes = QtWidgets.QPushButton(self.centralwidget)
        self.default_changes.setObjectName("default_changes")
        self.horizontalLayout_3.addWidget(self.default_changes)
        self.save_changes = QtWidgets.QPushButton(self.centralwidget)
        self.save_changes.setObjectName("save_changes")
        self.horizontalLayout_3.addWidget(self.save_changes)
        self.cancel_changes = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_changes.setObjectName("cancel_changes")
        self.horizontalLayout_3.addWidget(self.cancel_changes)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        Settings.setCentralWidget(self.centralwidget)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.alphabet_toggle.setText(_translate("Settings", "Show Alphabet"))
        self.default_changes.setText(_translate("Settings", "Default"))
        self.save_changes.setText(_translate("Settings", "Save Changes"))
        self.cancel_changes.setText(_translate("Settings", "Cancel"))
