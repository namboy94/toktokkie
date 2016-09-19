# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/start_page.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StartPage(object):
    def setupUi(self, StartPage):
        StartPage.setObjectName("StartPage")
        StartPage.resize(594, 110)
        self.centralwidget = QtWidgets.QWidget(StartPage)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tv_series_manager = QtWidgets.QPushButton(self.centralwidget)
        self.tv_series_manager.setObjectName("tv_series_manager")
        self.gridLayout.addWidget(self.tv_series_manager, 1, 0, 1, 1)
        self.tv_series_renamer = QtWidgets.QPushButton(self.centralwidget)
        self.tv_series_renamer.setObjectName("tv_series_renamer")
        self.gridLayout.addWidget(self.tv_series_renamer, 0, 0, 1, 1)
        self.xdcc_downloader = QtWidgets.QPushButton(self.centralwidget)
        self.xdcc_downloader.setObjectName("xdcc_downloader")
        self.gridLayout.addWidget(self.xdcc_downloader, 0, 1, 1, 1)
        self.manga_downloader = QtWidgets.QPushButton(self.centralwidget)
        self.manga_downloader.setObjectName("manga_downloader")
        self.gridLayout.addWidget(self.manga_downloader, 0, 2, 1, 1)
        self.folder_iconizer = QtWidgets.QPushButton(self.centralwidget)
        self.folder_iconizer.setObjectName("folder_iconizer")
        self.gridLayout.addWidget(self.folder_iconizer, 1, 4, 1, 1)
        self.xdcc_download_manager = QtWidgets.QPushButton(self.centralwidget)
        self.xdcc_download_manager.setObjectName("xdcc_download_manager")
        self.gridLayout.addWidget(self.xdcc_download_manager, 1, 1, 1, 1)
        self.manga_download_manager = QtWidgets.QPushButton(self.centralwidget)
        self.manga_download_manager.setObjectName("manga_download_manager")
        self.gridLayout.addWidget(self.manga_download_manager, 1, 2, 1, 1)
        StartPage.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(StartPage)
        self.statusbar.setObjectName("statusbar")
        StartPage.setStatusBar(self.statusbar)

        self.retranslateUi(StartPage)
        QtCore.QMetaObject.connectSlotsByName(StartPage)

    def retranslateUi(self, StartPage):
        _translate = QtCore.QCoreApplication.translate
        StartPage.setWindowTitle(_translate("StartPage", "MainWindow"))
        self.tv_series_manager.setText(_translate("StartPage", "TV Series Manager"))
        self.tv_series_renamer.setText(_translate("StartPage", "TV Series Renamer"))
        self.xdcc_downloader.setText(_translate("StartPage", "XDCC Downloader"))
        self.manga_downloader.setText(_translate("StartPage", "Manga Downloader"))
        self.folder_iconizer.setText(_translate("StartPage", "Folder Iconizer"))
        self.xdcc_download_manager.setText(_translate("StartPage", "XDCC Download Manager"))
        self.manga_download_manager.setText(_translate("StartPage", "Manga Download Manager"))

