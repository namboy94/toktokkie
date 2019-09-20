# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toktokkie/gui/qt_designer/tv_season_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TvSeasonWidget(object):
    def setupUi(self, TvSeasonWidget):
        TvSeasonWidget.setObjectName("TvSeasonWidget")
        TvSeasonWidget.resize(661, 369)
        self.gridLayout = QtWidgets.QGridLayout(TvSeasonWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.name = QtWidgets.QLabel(TvSeasonWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.name.setFont(font)
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.open_directory_button = QtWidgets.QPushButton(TvSeasonWidget)
        self.open_directory_button.setObjectName("open_directory_button")
        self.gridLayout.addWidget(self.open_directory_button, 5, 0, 1, 1)
        self.icon_label = QtWidgets.QLabel(TvSeasonWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon_label.sizePolicy().hasHeightForWidth())
        self.icon_label.setSizePolicy(sizePolicy)
        self.icon_label.setMinimumSize(QtCore.QSize(256, 256))
        self.icon_label.setMaximumSize(QtCore.QSize(256, 256))
        self.icon_label.setText("")
        self.icon_label.setPixmap(QtGui.QPixmap("../../../../metadata/Breaking Bad/.meta/icons/main.png"))
        self.icon_label.setScaledContents(True)
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_label.setObjectName("icon_label")
        self.gridLayout.addWidget(self.icon_label, 3, 0, 1, 1)
        self.frame = QtWidgets.QFrame(TvSeasonWidget)
        self.frame.setEnabled(True)
        self.frame.setMaximumSize(QtCore.QSize(500, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tvdb_id_edit = QtWidgets.QLineEdit(self.frame)
        self.tvdb_id_edit.setText("")
        self.tvdb_id_edit.setObjectName("tvdb_id_edit")
        self.gridLayout_2.addWidget(self.tvdb_id_edit, 1, 1, 1, 2)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.amount_of_episodes_label = QtWidgets.QLabel(self.frame_2)
        self.amount_of_episodes_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.amount_of_episodes_label.setText("")
        self.amount_of_episodes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amount_of_episodes_label.setObjectName("amount_of_episodes_label")
        self.gridLayout_3.addWidget(self.amount_of_episodes_label, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 1, 0, 1, 1)
        self.episode_list = QtWidgets.QListWidget(self.frame_2)
        self.episode_list.setObjectName("episode_list")
        self.gridLayout_3.addWidget(self.episode_list, 2, 0, 1, 2)
        self.gridLayout_2.addWidget(self.frame_2, 3, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.confirm_changes_button = QtWidgets.QPushButton(self.frame)
        self.confirm_changes_button.setObjectName("confirm_changes_button")
        self.gridLayout_2.addWidget(self.confirm_changes_button, 4, 1, 1, 1)
        self.tvdb_url_button = QtWidgets.QPushButton(self.frame)
        self.tvdb_url_button.setObjectName("tvdb_url_button")
        self.gridLayout_2.addWidget(self.tvdb_url_button, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.season_name = QtWidgets.QLabel(self.frame)
        self.season_name.setAlignment(QtCore.Qt.AlignCenter)
        self.season_name.setObjectName("season_name")
        self.gridLayout_2.addWidget(self.season_name, 0, 0, 1, 4)
        self.gridLayout.addWidget(self.frame, 0, 1, 7, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)

        self.retranslateUi(TvSeasonWidget)
        QtCore.QMetaObject.connectSlotsByName(TvSeasonWidget)
        TvSeasonWidget.setTabOrder(self.tvdb_id_edit, self.tvdb_url_button)
        TvSeasonWidget.setTabOrder(self.tvdb_url_button, self.confirm_changes_button)

    def retranslateUi(self, TvSeasonWidget):
        _translate = QtCore.QCoreApplication.translate
        TvSeasonWidget.setWindowTitle(_translate("TvSeasonWidget", "Form"))
        self.name.setText(_translate("TvSeasonWidget", "Name"))
        self.open_directory_button.setText(_translate("TvSeasonWidget", "Open Directory"))
        self.label_12.setText(_translate("TvSeasonWidget", "Amount of Episodes"))
        self.confirm_changes_button.setText(_translate("TvSeasonWidget", "Confirm Changes"))
        self.tvdb_url_button.setText(_translate("TvSeasonWidget", "Go"))
        self.label_2.setText(_translate("TvSeasonWidget", "TheTVDB.com"))
        self.season_name.setText(_translate("TvSeasonWidget", "Season Name"))
