# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toktokkie/ui/qt/qt_designer/xdcc_update_configurator.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_XDCCUpdateConfiguratorWindow(object):
    def setupUi(self, XDCCUpdateConfiguratorWindow):
        XDCCUpdateConfiguratorWindow.setObjectName("XDCCUpdateConfiguratorWindow")
        XDCCUpdateConfiguratorWindow.resize(639, 407)
        self.centralwidget = QtWidgets.QWidget(XDCCUpdateConfiguratorWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.naming_scheme_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.naming_scheme_combo_box.setObjectName("naming_scheme_combo_box")
        self.gridLayout.addWidget(self.naming_scheme_combo_box, 6, 4, 1, 2)
        self.bot_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.bot_edit.setObjectName("bot_edit")
        self.gridLayout.addWidget(self.bot_edit, 3, 4, 1, 2)
        self.new_button = QtWidgets.QPushButton(self.centralwidget)
        self.new_button.setObjectName("new_button")
        self.gridLayout.addWidget(self.new_button, 11, 1, 1, 1)
        self.quality_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.quality_combo_box.setObjectName("quality_combo_box")
        self.quality_combo_box.addItem("")
        self.quality_combo_box.addItem("")
        self.quality_combo_box.addItem("")
        self.gridLayout.addWidget(self.quality_combo_box, 2, 4, 1, 2)
        self.season_spin_box = QtWidgets.QSpinBox(self.centralwidget)
        self.season_spin_box.setObjectName("season_spin_box")
        self.gridLayout.addWidget(self.season_spin_box, 4, 4, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 3, 1, 1)
        self.search_name_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_name_edit.setObjectName("search_name_edit")
        self.gridLayout.addWidget(self.search_name_edit, 1, 4, 1, 2)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setObjectName("save_button")
        self.gridLayout.addWidget(self.save_button, 12, 1, 1, 1)
        self.load_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 12, 0, 1, 1)
        self.delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_button.setObjectName("delete_button")
        self.gridLayout.addWidget(self.delete_button, 11, 0, 1, 1)
        self.directory_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.directory_edit.setObjectName("directory_edit")
        self.gridLayout.addWidget(self.directory_edit, 0, 4, 1, 2)
        self.series_list = QtWidgets.QListWidget(self.centralwidget)
        self.series_list.setObjectName("series_list")
        self.gridLayout.addWidget(self.series_list, 0, 0, 11, 2)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
        self.search_engine_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.search_engine_combo_box.setObjectName("search_engine_combo_box")
        self.gridLayout.addWidget(self.search_engine_combo_box, 5, 4, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 3, 1, 1)
        self.pattern_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.pattern_combo_box.setObjectName("pattern_combo_box")
        self.gridLayout.addWidget(self.pattern_combo_box, 7, 4, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 3, 1, 1)
        self.confirm_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirm_button.setObjectName("confirm_button")
        self.gridLayout.addWidget(self.confirm_button, 12, 5, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 5, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 8, 3, 1, 1)
        self.episode_offset_spinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.episode_offset_spinbox.setObjectName("episode_offset_spinbox")
        self.gridLayout.addWidget(self.episode_offset_spinbox, 8, 4, 1, 2)
        XDCCUpdateConfiguratorWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(XDCCUpdateConfiguratorWindow)
        self.statusbar.setObjectName("statusbar")
        XDCCUpdateConfiguratorWindow.setStatusBar(self.statusbar)

        self.retranslateUi(XDCCUpdateConfiguratorWindow)
        QtCore.QMetaObject.connectSlotsByName(XDCCUpdateConfiguratorWindow)

    def retranslateUi(self, XDCCUpdateConfiguratorWindow):
        _translate = QtCore.QCoreApplication.translate
        XDCCUpdateConfiguratorWindow.setWindowTitle(_translate("XDCCUpdateConfiguratorWindow", "XDCC Update Configurator"))
        self.new_button.setText(_translate("XDCCUpdateConfiguratorWindow", "New"))
        self.quality_combo_box.setItemText(0, _translate("XDCCUpdateConfiguratorWindow", "480p"))
        self.quality_combo_box.setItemText(1, _translate("XDCCUpdateConfiguratorWindow", "720p"))
        self.quality_combo_box.setItemText(2, _translate("XDCCUpdateConfiguratorWindow", "1080p"))
        self.label_6.setText(_translate("XDCCUpdateConfiguratorWindow", "Search Engines"))
        self.save_button.setText(_translate("XDCCUpdateConfiguratorWindow", "Save"))
        self.load_button.setText(_translate("XDCCUpdateConfiguratorWindow", "Load"))
        self.delete_button.setText(_translate("XDCCUpdateConfiguratorWindow", "Delete"))
        self.label_7.setText(_translate("XDCCUpdateConfiguratorWindow", "Naming Scheme"))
        self.label.setText(_translate("XDCCUpdateConfiguratorWindow", "Directory"))
        self.label_2.setText(_translate("XDCCUpdateConfiguratorWindow", "Search Name"))
        self.label_3.setText(_translate("XDCCUpdateConfiguratorWindow", "Quality"))
        self.label_4.setText(_translate("XDCCUpdateConfiguratorWindow", "Bot"))
        self.label_5.setText(_translate("XDCCUpdateConfiguratorWindow", "Season"))
        self.confirm_button.setText(_translate("XDCCUpdateConfiguratorWindow", "Confirm Changes"))
        self.label_8.setText(_translate("XDCCUpdateConfiguratorWindow", "Pattern"))
        self.label_9.setText(_translate("XDCCUpdateConfiguratorWindow", "Episode Offset"))

