# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toktokkie/ui/qt/qt_designer/anime_series_config.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AnimeSeriesConfig(object):
    def setupUi(self, AnimeSeriesConfig):
        AnimeSeriesConfig.setObjectName("AnimeSeriesConfig")
        AnimeSeriesConfig.resize(1036, 680)
        self.gridLayout = QtWidgets.QGridLayout(AnimeSeriesConfig)
        self.gridLayout.setObjectName("gridLayout")
        self.series_name_edit = QtWidgets.QLineEdit(AnimeSeriesConfig)
        self.series_name_edit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.series_name_edit.sizePolicy().hasHeightForWidth())
        self.series_name_edit.setSizePolicy(sizePolicy)
        self.series_name_edit.setMinimumSize(QtCore.QSize(134, 0))
        self.series_name_edit.setFrame(False)
        self.series_name_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.series_name_edit.setObjectName("series_name_edit")
        self.gridLayout.addWidget(self.series_name_edit, 1, 0, 1, 1)
        self.folder_icon_label = QtWidgets.QLabel(AnimeSeriesConfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.folder_icon_label.sizePolicy().hasHeightForWidth())
        self.folder_icon_label.setSizePolicy(sizePolicy)
        self.folder_icon_label.setMaximumSize(QtCore.QSize(5120, 5120))
        self.folder_icon_label.setText("")
        self.folder_icon_label.setPixmap(QtGui.QPixmap("../../../../../../../Downloads/pokemon_folder_icon_by_mikromike-d8mldi8.png"))
        self.folder_icon_label.setScaledContents(False)
        self.folder_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.folder_icon_label.setObjectName("folder_icon_label")
        self.gridLayout.addWidget(self.folder_icon_label, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.frame = QtWidgets.QFrame(AnimeSeriesConfig)
        self.frame.setEnabled(True)
        self.frame.setMaximumSize(QtCore.QSize(500, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.confirm_changes_button = QtWidgets.QPushButton(self.frame)
        self.confirm_changes_button.setObjectName("confirm_changes_button")
        self.gridLayout_2.addWidget(self.confirm_changes_button, 11, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_15 = QtWidgets.QLabel(self.frame_2)
        self.label_15.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_2)
        self.label_10.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)
        self.mal_runtime_label = QtWidgets.QLabel(self.frame_2)
        self.mal_runtime_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_runtime_label.setText("")
        self.mal_runtime_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_runtime_label.setWordWrap(True)
        self.mal_runtime_label.setObjectName("mal_runtime_label")
        self.gridLayout_3.addWidget(self.mal_runtime_label, 7, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.frame_2)
        self.label_18.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 6, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.frame_2)
        self.label_19.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout_3.addWidget(self.label_19, 8, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.frame_2)
        self.label_16.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 7, 0, 1, 1)
        self.mal_source_label = QtWidgets.QLabel(self.frame_2)
        self.mal_source_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_source_label.setText("")
        self.mal_source_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_source_label.setObjectName("mal_source_label")
        self.gridLayout_3.addWidget(self.mal_source_label, 5, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 4, 0, 1, 1)
        self.mal_status_label = QtWidgets.QLabel(self.frame_2)
        self.mal_status_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_status_label.setText("")
        self.mal_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_status_label.setObjectName("mal_status_label")
        self.gridLayout_3.addWidget(self.mal_status_label, 2, 1, 1, 1)
        self.mal_aired_label = QtWidgets.QLabel(self.frame_2)
        self.mal_aired_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_aired_label.setText("")
        self.mal_aired_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_aired_label.setObjectName("mal_aired_label")
        self.gridLayout_3.addWidget(self.mal_aired_label, 3, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_2)
        self.label_14.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 5, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.frame_2)
        self.label_17.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 1, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.frame_2)
        self.label_20.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 9, 0, 1, 1)
        self.mal_type_label = QtWidgets.QLabel(self.frame_2)
        self.mal_type_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_type_label.setText("")
        self.mal_type_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_type_label.setObjectName("mal_type_label")
        self.gridLayout_3.addWidget(self.mal_type_label, 0, 1, 1, 1)
        self.mal_episodes_label = QtWidgets.QLabel(self.frame_2)
        self.mal_episodes_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_episodes_label.setText("")
        self.mal_episodes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_episodes_label.setObjectName("mal_episodes_label")
        self.gridLayout_3.addWidget(self.mal_episodes_label, 1, 1, 1, 1)
        self.mal_genres_label = QtWidgets.QLabel(self.frame_2)
        self.mal_genres_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_genres_label.setText("")
        self.mal_genres_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_genres_label.setObjectName("mal_genres_label")
        self.gridLayout_3.addWidget(self.mal_genres_label, 6, 1, 1, 1)
        self.mal_score_label = QtWidgets.QLabel(self.frame_2)
        self.mal_score_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_score_label.setText("")
        self.mal_score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_score_label.setObjectName("mal_score_label")
        self.gridLayout_3.addWidget(self.mal_score_label, 8, 1, 1, 1)
        self.mal_ranking_label = QtWidgets.QLabel(self.frame_2)
        self.mal_ranking_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_ranking_label.setText("")
        self.mal_ranking_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_ranking_label.setObjectName("mal_ranking_label")
        self.gridLayout_3.addWidget(self.mal_ranking_label, 9, 1, 1, 1)
        self.mal_studios_label = QtWidgets.QLabel(self.frame_2)
        self.mal_studios_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mal_studios_label.setText("")
        self.mal_studios_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mal_studios_label.setObjectName("mal_studios_label")
        self.gridLayout_3.addWidget(self.mal_studios_label, 4, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 10, 0, 1, 4)
        self.resolution_three_edit_y = QtWidgets.QLineEdit(self.frame)
        self.resolution_three_edit_y.setMinimumSize(QtCore.QSize(146, 0))
        self.resolution_three_edit_y.setText("")
        self.resolution_three_edit_y.setObjectName("resolution_three_edit_y")
        self.gridLayout_2.addWidget(self.resolution_three_edit_y, 6, 3, 1, 1)
        self.tags_edit = QtWidgets.QLineEdit(self.frame)
        self.tags_edit.setText("")
        self.tags_edit.setObjectName("tags_edit")
        self.gridLayout_2.addWidget(self.tags_edit, 1, 1, 1, 3)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 7, 0, 1, 1)
        self.audio_language_edit = QtWidgets.QLineEdit(self.frame)
        self.audio_language_edit.setText("")
        self.audio_language_edit.setObjectName("audio_language_edit")
        self.gridLayout_2.addWidget(self.audio_language_edit, 7, 1, 1, 3)
        self.tvdb_url_edit = QtWidgets.QLineEdit(self.frame)
        self.tvdb_url_edit.setText("")
        self.tvdb_url_edit.setObjectName("tvdb_url_edit")
        self.gridLayout_2.addWidget(self.tvdb_url_edit, 2, 1, 1, 2)
        self.resolution_one_edit_x = QtWidgets.QLineEdit(self.frame)
        self.resolution_one_edit_x.setText("")
        self.resolution_one_edit_x.setObjectName("resolution_one_edit_x")
        self.gridLayout_2.addWidget(self.resolution_one_edit_x, 4, 1, 1, 1)
        self.resolution_three_edit_x = QtWidgets.QLineEdit(self.frame)
        self.resolution_three_edit_x.setText("")
        self.resolution_three_edit_x.setObjectName("resolution_three_edit_x")
        self.gridLayout_2.addWidget(self.resolution_three_edit_x, 6, 1, 1, 1)
        self.resolution_one_edit_y = QtWidgets.QLineEdit(self.frame)
        self.resolution_one_edit_y.setMinimumSize(QtCore.QSize(146, 0))
        self.resolution_one_edit_y.setText("")
        self.resolution_one_edit_y.setObjectName("resolution_one_edit_y")
        self.gridLayout_2.addWidget(self.resolution_one_edit_y, 4, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.media_type_combo_box = QtWidgets.QComboBox(self.frame)
        self.media_type_combo_box.setObjectName("media_type_combo_box")
        self.gridLayout_2.addWidget(self.media_type_combo_box, 0, 1, 1, 3)
        self.resolution_two_edit_y = QtWidgets.QLineEdit(self.frame)
        self.resolution_two_edit_y.setMinimumSize(QtCore.QSize(146, 0))
        self.resolution_two_edit_y.setText("")
        self.resolution_two_edit_y.setObjectName("resolution_two_edit_y")
        self.gridLayout_2.addWidget(self.resolution_two_edit_y, 5, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 3, 1)
        self.tvdb_url_button = QtWidgets.QPushButton(self.frame)
        self.tvdb_url_button.setObjectName("tvdb_url_button")
        self.gridLayout_2.addWidget(self.tvdb_url_button, 2, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.subtitle_language_edit = QtWidgets.QLineEdit(self.frame)
        self.subtitle_language_edit.setText("")
        self.subtitle_language_edit.setObjectName("subtitle_language_edit")
        self.gridLayout_2.addWidget(self.subtitle_language_edit, 8, 1, 1, 3)
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 5, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 6, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 9, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 8, 0, 1, 1)
        self.resolution_two_edit_x = QtWidgets.QLineEdit(self.frame)
        self.resolution_two_edit_x.setText("")
        self.resolution_two_edit_x.setObjectName("resolution_two_edit_x")
        self.gridLayout_2.addWidget(self.resolution_two_edit_x, 5, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 4, 2, 1, 1)
        self.myanimelist_url_button = QtWidgets.QPushButton(self.frame)
        self.myanimelist_url_button.setObjectName("myanimelist_url_button")
        self.gridLayout_2.addWidget(self.myanimelist_url_button, 3, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setFrameShape(QtWidgets.QFrame.Box)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 3, 0, 1, 1)
        self.myanimelist_url_edit = QtWidgets.QLineEdit(self.frame)
        self.myanimelist_url_edit.setObjectName("myanimelist_url_edit")
        self.gridLayout_2.addWidget(self.myanimelist_url_edit, 3, 1, 1, 2)
        self.gridLayout.addWidget(self.frame, 0, 1, 7, 1)
        self.open_directory_button = QtWidgets.QPushButton(AnimeSeriesConfig)
        self.open_directory_button.setObjectName("open_directory_button")
        self.gridLayout.addWidget(self.open_directory_button, 5, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)

        self.retranslateUi(AnimeSeriesConfig)
        QtCore.QMetaObject.connectSlotsByName(AnimeSeriesConfig)
        AnimeSeriesConfig.setTabOrder(self.series_name_edit, self.media_type_combo_box)
        AnimeSeriesConfig.setTabOrder(self.media_type_combo_box, self.tags_edit)
        AnimeSeriesConfig.setTabOrder(self.tags_edit, self.tvdb_url_edit)
        AnimeSeriesConfig.setTabOrder(self.tvdb_url_edit, self.tvdb_url_button)
        AnimeSeriesConfig.setTabOrder(self.tvdb_url_button, self.resolution_one_edit_x)
        AnimeSeriesConfig.setTabOrder(self.resolution_one_edit_x, self.resolution_one_edit_y)
        AnimeSeriesConfig.setTabOrder(self.resolution_one_edit_y, self.resolution_two_edit_x)
        AnimeSeriesConfig.setTabOrder(self.resolution_two_edit_x, self.resolution_two_edit_y)
        AnimeSeriesConfig.setTabOrder(self.resolution_two_edit_y, self.resolution_three_edit_x)
        AnimeSeriesConfig.setTabOrder(self.resolution_three_edit_x, self.resolution_three_edit_y)
        AnimeSeriesConfig.setTabOrder(self.resolution_three_edit_y, self.audio_language_edit)
        AnimeSeriesConfig.setTabOrder(self.audio_language_edit, self.subtitle_language_edit)
        AnimeSeriesConfig.setTabOrder(self.subtitle_language_edit, self.confirm_changes_button)

    def retranslateUi(self, AnimeSeriesConfig):
        _translate = QtCore.QCoreApplication.translate
        AnimeSeriesConfig.setWindowTitle(_translate("AnimeSeriesConfig", "Form"))
        self.series_name_edit.setText(_translate("AnimeSeriesConfig", "Series Name"))
        self.confirm_changes_button.setText(_translate("AnimeSeriesConfig", "Confirm Changes"))
        self.label_15.setText(_translate("AnimeSeriesConfig", "Type"))
        self.label_10.setText(_translate("AnimeSeriesConfig", "Aired"))
        self.label_8.setText(_translate("AnimeSeriesConfig", "Status"))
        self.label_18.setText(_translate("AnimeSeriesConfig", "Genres"))
        self.label_19.setText(_translate("AnimeSeriesConfig", "myanimelist.net Score"))
        self.label_16.setText(_translate("AnimeSeriesConfig", "Runtime"))
        self.label_12.setText(_translate("AnimeSeriesConfig", "Studios"))
        self.label_14.setText(_translate("AnimeSeriesConfig", "Source"))
        self.label_17.setText(_translate("AnimeSeriesConfig", "Episodes"))
        self.label_20.setText(_translate("AnimeSeriesConfig", "myanimelist.net Ranking"))
        self.label_6.setText(_translate("AnimeSeriesConfig", "Audio Languages"))
        self.label_2.setText(_translate("AnimeSeriesConfig", "TheTVDB.com"))
        self.label_5.setText(_translate("AnimeSeriesConfig", "Resolutions"))
        self.tvdb_url_button.setText(_translate("AnimeSeriesConfig", "Go"))
        self.label_3.setText(_translate("AnimeSeriesConfig", "Tags"))
        self.label_4.setText(_translate("AnimeSeriesConfig", "Media Type"))
        self.label_9.setText(_translate("AnimeSeriesConfig", "X"))
        self.label_11.setText(_translate("AnimeSeriesConfig", "X"))
        self.label_7.setText(_translate("AnimeSeriesConfig", "Subtitle Languages"))
        self.label.setText(_translate("AnimeSeriesConfig", "X"))
        self.myanimelist_url_button.setText(_translate("AnimeSeriesConfig", "Go"))
        self.label_13.setText(_translate("AnimeSeriesConfig", "myanimelist.net"))
        self.open_directory_button.setText(_translate("AnimeSeriesConfig", "Open Directory"))

