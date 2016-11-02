# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toktokkie/ui/qt/qt_designer/iconizer.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FolderIconizerWindow(object):
    def setupUi(self, FolderIconizerWindow):
        FolderIconizerWindow.setObjectName("FolderIconizerWindow")
        FolderIconizerWindow.resize(513, 62)
        self.centralwidget = QtWidgets.QWidget(FolderIconizerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.directory_path_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.directory_path_edit.setObjectName("directory_path_edit")
        self.gridLayout.addWidget(self.directory_path_edit, 0, 1, 1, 1)
        self.browse_directory_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_directory_button.setObjectName("browse_directory_button")
        self.gridLayout.addWidget(self.browse_directory_button, 0, 0, 1, 1)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 0, 2, 1, 1)
        FolderIconizerWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FolderIconizerWindow)
        self.statusbar.setObjectName("statusbar")
        FolderIconizerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(FolderIconizerWindow)
        QtCore.QMetaObject.connectSlotsByName(FolderIconizerWindow)

    def retranslateUi(self, FolderIconizerWindow):
        _translate = QtCore.QCoreApplication.translate
        FolderIconizerWindow.setWindowTitle(_translate("FolderIconizerWindow", "Folder Iconizer"))
        self.browse_directory_button.setText(_translate("FolderIconizerWindow", "Browse"))
        self.start_button.setText(_translate("FolderIconizerWindow", "Start"))

