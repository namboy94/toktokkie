# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toktokkie/ui/qt/qt_designer/start_page.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StartPageWindow(object):
    def setupUi(self, StartPageWindow):
        StartPageWindow.setObjectName("StartPageWindow")
        StartPageWindow.resize(352, 178)
        self.centralwidget = QtWidgets.QWidget(StartPageWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.folder_iconizer = QtWidgets.QPushButton(self.centralwidget)
        self.folder_iconizer.setObjectName("folder_iconizer")
        self.gridLayout.addWidget(self.folder_iconizer, 2, 0, 1, 1)
        self.tv_series_renamer = QtWidgets.QPushButton(self.centralwidget)
        self.tv_series_renamer.setObjectName("tv_series_renamer")
        self.gridLayout.addWidget(self.tv_series_renamer, 1, 0, 1, 1)
        StartPageWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(StartPageWindow)
        self.statusbar.setObjectName("statusbar")
        StartPageWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartPageWindow)
        QtCore.QMetaObject.connectSlotsByName(StartPageWindow)

    def retranslateUi(self, StartPageWindow):
        _translate = QtCore.QCoreApplication.translate
        StartPageWindow.setWindowTitle(_translate("StartPageWindow", "Toktokkie"))
        self.folder_iconizer.setText(_translate("StartPageWindow", "Folder Iconizer"))
        self.tv_series_renamer.setText(_translate("StartPageWindow", "TV Series Renamer"))

