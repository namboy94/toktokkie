# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/tv_series_renamer.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Renamer(object):
    def setupUi(self, Renamer):
        Renamer.setObjectName("Renamer")
        Renamer.resize(753, 378)
        self.centralwidget = QtWidgets.QWidget(Renamer)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setObjectName("browse_button")
        self.gridLayout.addWidget(self.browse_button, 0, 0, 1, 1)
        self.confirm_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirm_button.setObjectName("confirm_button")
        self.gridLayout.addWidget(self.confirm_button, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 0, 5, 1, 1)
        self.rename_list = QtWidgets.QTreeWidget(self.centralwidget)
        self.rename_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.rename_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.rename_list.setObjectName("rename_list")
        self.gridLayout.addWidget(self.rename_list, 1, 0, 1, 6)
        self.selection_remover_button = QtWidgets.QPushButton(self.centralwidget)
        self.selection_remover_button.setMaximumSize(QtCore.QSize(156, 16777215))
        self.selection_remover_button.setObjectName("selection_remover_button")
        self.gridLayout.addWidget(self.selection_remover_button, 2, 4, 1, 2)
        self.scheme_selector = QtWidgets.QComboBox(self.centralwidget)
        self.scheme_selector.setMinimumSize(QtCore.QSize(200, 0))
        self.scheme_selector.setObjectName("scheme_selector")
        self.gridLayout.addWidget(self.scheme_selector, 0, 3, 1, 1)
        self.selection_inverter_button = QtWidgets.QPushButton(self.centralwidget)
        self.selection_inverter_button.setObjectName("selection_inverter_button")
        self.gridLayout.addWidget(self.selection_inverter_button, 2, 3, 1, 1)
        self.meta_warning_label = QtWidgets.QLabel(self.centralwidget)
        self.meta_warning_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.meta_warning_label.setWordWrap(True)
        self.meta_warning_label.setObjectName("meta_warning_label")
        self.gridLayout.addWidget(self.meta_warning_label, 2, 0, 1, 3)
        self.directory_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.directory_entry.setObjectName("directory_entry")
        self.gridLayout.addWidget(self.directory_entry, 0, 1, 1, 1)
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
        self.cancel_button.setText(_translate("Renamer", "Cancel"))
        self.rename_list.headerItem().setText(0, _translate("Renamer", "Old Name"))
        self.rename_list.headerItem().setText(1, _translate("Renamer", "New Name"))
        self.selection_remover_button.setText(_translate("Renamer", "Remove Selection"))
        self.scheme_selector.setToolTip(_translate("Renamer", "<html><head/><body><p>The naming scheme used for renaming the episodes</p></body></html>"))
        self.selection_inverter_button.setText(_translate("Renamer", "Invert Selection"))
        self.meta_warning_label.setText(_translate("Renamer", "<html><head/><body><p><span style=\" color:#ff0000;\">Warning: Selected Directory does not contain any .meta subdirectories with type \'tv_series\'</span></p></body></html>"))

