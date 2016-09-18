# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tv_series_renamer.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Renamer(object):
    def setupUi(self, Renamer):
        Renamer.setObjectName("Renamer")
        Renamer.resize(853, 288)
        self.centralwidget = QtWidgets.QWidget(Renamer)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setObjectName("browse_button")
        self.gridLayout.addWidget(self.browse_button, 0, 0, 1, 1)
        self.directory_path_edit = QtWidgets.QTextEdit(self.centralwidget)
        self.directory_path_edit.setMinimumSize(QtCore.QSize(191, 0))
        self.directory_path_edit.setMaximumSize(QtCore.QSize(1777215, 35))
        self.directory_path_edit.setObjectName("directory_path_edit")
        self.gridLayout.addWidget(self.directory_path_edit, 0, 1, 1, 1)
        self.confirm_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirm_button.setObjectName("confirm_button")
        self.gridLayout.addWidget(self.confirm_button, 0, 4, 1, 1)
        self.fetch_button = QtWidgets.QPushButton(self.centralwidget)
        self.fetch_button.setObjectName("fetch_button")
        self.gridLayout.addWidget(self.fetch_button, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 0, 5, 1, 1)
        self.changelist = QtWidgets.QTreeWidget(self.centralwidget)
        self.changelist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.changelist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.changelist.setObjectName("changelist")
        self.gridLayout.addWidget(self.changelist, 1, 0, 1, 6)
        Renamer.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Renamer)
        self.statusbar.setObjectName("statusbar")
        Renamer.setStatusBar(self.statusbar)

        self.retranslateUi(Renamer)
        QtCore.QMetaObject.connectSlotsByName(Renamer)

    def retranslateUi(self, Renamer):
        _translate = QtCore.QCoreApplication.translate
        Renamer.setWindowTitle(_translate("Renamer", "MainWindow"))
        self.browse_button.setText(_translate("Renamer", "Browse"))
        self.confirm_button.setText(_translate("Renamer", "Confirm"))
        self.fetch_button.setText(_translate("Renamer", "Fetch"))
        self.cancel_button.setText(_translate("Renamer", "Cancel"))
        self.changelist.headerItem().setText(0, _translate("Renamer", "Old Name"))
        self.changelist.headerItem().setText(1, _translate("Renamer", "New Name"))

