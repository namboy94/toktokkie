# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toktokkie/gui/qt_designer/tv_show_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TvSeriesWidget(object):
    def setupUi(self, TvSeriesWidget):
        TvSeriesWidget.setObjectName("TvSeriesWidget")
        TvSeriesWidget.resize(661, 369)
        self.gridLayout = QtWidgets.QGridLayout(TvSeriesWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.name = QtWidgets.QLabel(TvSeriesWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.name.setFont(font)
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.open_directory_button = QtWidgets.QPushButton(TvSeriesWidget)
        self.open_directory_button.setObjectName("open_directory_button")
        self.gridLayout.addWidget(self.open_directory_button, 5, 0, 1, 1)
        self.icon_label = QtWidgets.QLabel(TvSeriesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon_label.sizePolicy().hasHeightForWidth())
        self.icon_label.setSizePolicy(sizePolicy)
        self.icon_label.setMinimumSize(QtCore.QSize(256, 256))
        self.icon_label.setMaximumSize(QtCore.QSize(256, 256))
        self.icon_label.setText("")
        self.icon_label.setPixmap(QtGui.QPixmap("../../../../../Downloads/pokemon_folder_icon_by_mikromike-d8mldi8.png"))
        self.icon_label.setScaledContents(True)
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_label.setObjectName("icon_label")
        self.gridLayout.addWidget(self.icon_label, 3, 0, 1, 1)
        self.frame = QtWidgets.QFrame(TvSeriesWidget)
        self.frame.setEnabled(True)
        self.frame.setMaximumSize(QtCore.QSize(500, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        self.gridLayout_3.addWidget(self.amount_of_episodes_label, 3, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_2)
        self.label_10.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.genres_label = QtWidgets.QLabel(self.frame_2)
        self.genres_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.genres_label.setText("")
        self.genres_label.setAlignment(QtCore.Qt.AlignCenter)
        self.genres_label.setWordWrap(True)
        self.genres_label.setObjectName("genres_label")
        self.gridLayout_3.addWidget(self.genres_label, 5, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.frame_2)
        self.label_16.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 5, 0, 1, 1)
        self.amount_of_seasons_label = QtWidgets.QLabel(self.frame_2)
        self.amount_of_seasons_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.amount_of_seasons_label.setText("")
        self.amount_of_seasons_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amount_of_seasons_label.setObjectName("amount_of_seasons_label")
        self.gridLayout_3.addWidget(self.amount_of_seasons_label, 4, 1, 1, 1)
        self.first_aired_label = QtWidgets.QLabel(self.frame_2)
        self.first_aired_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.first_aired_label.setText("")
        self.first_aired_label.setAlignment(QtCore.Qt.AlignCenter)
        self.first_aired_label.setObjectName("first_aired_label")
        self.gridLayout_3.addWidget(self.first_aired_label, 1, 1, 1, 1)
        self.episode_length_label = QtWidgets.QLabel(self.frame_2)
        self.episode_length_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.episode_length_label.setText("")
        self.episode_length_label.setAlignment(QtCore.Qt.AlignCenter)
        self.episode_length_label.setObjectName("episode_length_label")
        self.gridLayout_3.addWidget(self.episode_length_label, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_2)
        self.label_14.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 4, 0, 1, 4)
        self.tags_edit = QtWidgets.QLineEdit(self.frame)
        self.tags_edit.setText("")
        self.tags_edit.setObjectName("tags_edit")
        self.gridLayout_2.addWidget(self.tags_edit, 1, 1, 1, 3)
        self.tvdb_url_button = QtWidgets.QPushButton(self.frame)
        self.tvdb_url_button.setObjectName("tvdb_url_button")
        self.gridLayout_2.addWidget(self.tvdb_url_button, 2, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 3, 0, 1, 1)
        self.confirm_changes_button = QtWidgets.QPushButton(self.frame)
        self.confirm_changes_button.setObjectName("confirm_changes_button")
        self.gridLayout_2.addWidget(self.confirm_changes_button, 5, 1, 1, 1)
        self.tvdb_id_edit = QtWidgets.QLineEdit(self.frame)
        self.tvdb_id_edit.setText("")
        self.tvdb_id_edit.setObjectName("tvdb_id_edit")
        self.gridLayout_2.addWidget(self.tvdb_id_edit, 2, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.media_type_label = QtWidgets.QLabel(self.frame)
        self.media_type_label.setAlignment(QtCore.Qt.AlignCenter)
        self.media_type_label.setObjectName("media_type_label")
        self.gridLayout_2.addWidget(self.media_type_label, 0, 1, 1, 3)
        self.gridLayout.addWidget(self.frame, 0, 1, 7, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)

        self.retranslateUi(TvSeriesWidget)
        QtCore.QMetaObject.connectSlotsByName(TvSeriesWidget)
        TvSeriesWidget.setTabOrder(self.tags_edit, self.tvdb_id_edit)
        TvSeriesWidget.setTabOrder(self.tvdb_id_edit, self.tvdb_url_button)
        TvSeriesWidget.setTabOrder(self.tvdb_url_button, self.confirm_changes_button)

    def retranslateUi(self, TvSeriesWidget):
        _translate = QtCore.QCoreApplication.translate
        TvSeriesWidget.setWindowTitle(_translate("TvSeriesWidget", "Form"))
        self.name.setText(_translate("TvSeriesWidget", "Name"))
        self.open_directory_button.setText(_translate("TvSeriesWidget", "Open Directory"))
        self.label_10.setText(_translate("TvSeriesWidget", "Episode Runtime"))
        self.label_12.setText(_translate("TvSeriesWidget", "Amount of Episodes"))
        self.label_8.setText(_translate("TvSeriesWidget", "First Aired"))
        self.label_16.setText(_translate("TvSeriesWidget", "Genres"))
        self.label_14.setText(_translate("TvSeriesWidget", "Amount of Seasons"))
        self.tvdb_url_button.setText(_translate("TvSeriesWidget", "Go"))
        self.confirm_changes_button.setText(_translate("TvSeriesWidget", "Confirm Changes"))
        self.label_2.setText(_translate("TvSeriesWidget", "TheTVDB.com"))
        self.label_4.setText(_translate("TvSeriesWidget", "Media Type"))
        self.label_3.setText(_translate("TvSeriesWidget", "Tags"))
        self.media_type_label.setText(_translate("TvSeriesWidget", "Media Type"))
