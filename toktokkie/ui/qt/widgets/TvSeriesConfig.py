"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

import sys
import webbrowser
from copy import copy
from threading import Thread
from subprocess import Popen
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from toktokkie.utils.metadata.media_types.TvSeries import TvSeries
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager
from toktokkie.ui.qt.pyuic.tv_series_config import Ui_TvSeriesConfig


class TvSeriesConfig(QWidget, Ui_TvSeriesConfig):
    """
    Widget for a TV Series
    """

    def __init__(self, parent):
        """
        Initializes the widget
        
        :param parent: The window in which to display the widget
        """
        super().__init__(parent)
        self.setupUi(self)
        self.metadata = None

        self.confirm_changes_button.clicked.connect(self.save_data)
        self.tvdb_url_button.clicked.connect(self.open_tvdb_url)
        self.open_directory_button.clicked.connect(self.open_directory)

        for media_type in MetaDataManager.media_type_map:
            self.media_type_combo_box.addItem(media_type)

    def set_data(self, metadata: TvSeries, child_id: str):
        """
        Sets the data to be displayed here
        
        :param metadata: The TvSeries metadata object to be displayed here
        :param child_id: Specifies which subdirectory should be displayed
        
        :return: None
        """
        self.metadata = copy(metadata)
        if child_id != "main":
            self.metadata.set_child_extender("seasons", child_id)
        self.display_data()

    def save_data(self):
        """
        Saves the data currently stored in the UI elements to the info.json file
        :return: None
        """
        self.metadata.name = self.series_name_edit.text()
        self.metadata.media_type = self.media_type_combo_box.currentText()
        self.metadata.tags = self.tags_edit.text().split(",")
        self.metadata.tvdb_url = self.tvdb_url_edit.text()
        self.metadata.audio_langs = self.audio_language_edit.text().split(",")
        self.metadata.subtitle_langs = self.subtitle_language_edit.text().split(",")

        resolutions = []
        for i, widgets in enumerate([
            [self.resolution_one_edit_x, self.resolution_one_edit_y],
            [self.resolution_two_edit_x, self.resolution_two_edit_y],
            [self.resolution_three_edit_x, self.resolution_three_edit_y]
        ]):
            if widgets[0].text() and widgets[1].text():
                try:
                    resolutions.append({
                        "x": int(widgets[0].text()),
                        "y": int(widgets[1].text())
                    })
                except ValueError:
                    pass
        self.metadata.resolutions = resolutions  # Must be set here due to the setter method

        self.metadata.write_changes()
        self.display_data()

    def display_data(self):
        """
        Displays the data of a TvSeriesConfig
        :return: None
        """
        self.media_type_combo_box.setCurrentIndex(self.media_type_combo_box.findText(self.metadata.media_type))
        self.series_name_edit.setText(self.metadata.name)
        self.folder_icon_label.setPixmap(QPixmap(self.metadata.get_icon_path()))

        self.tags_edit.setText(", ".join(self.metadata.tags))
        self.tvdb_url_edit.setText(self.metadata.tvdb_url)
        self.audio_language_edit.setText(", ".join(self.metadata.audio_langs))
        self.subtitle_language_edit.setText(", ".join(self.metadata.subtitle_langs))

        for i, widgets in enumerate([
            [self.resolution_one_edit_x, self.resolution_one_edit_y],
            [self.resolution_two_edit_x, self.resolution_two_edit_y],
            [self.resolution_three_edit_x, self.resolution_three_edit_y]
        ]):
            if len(self.metadata.resolutions) > i:
                widgets[0].setText(str(self.metadata.resolutions[i]["x"]))
                widgets[1].setText(str(self.metadata.resolutions[i]["y"]))
            else:
                widgets[0].setText("")
                widgets[1].setText("")

        self.first_aired_label.setText("")
        self.episode_length_label.setText("")
        self.amount_of_episodes_label.setText("")
        self.amount_of_seasons_label.setText("")
        self.genres_label.setText("")

        def load_data():
            tvdb_data = self.metadata.load_tvdb_data()
            self.first_aired_label.setText(tvdb_data["firstaired"])
            self.episode_length_label.setText(tvdb_data["runtime"])
            self.amount_of_episodes_label.setText(str(tvdb_data["episode_count"]))
            self.amount_of_seasons_label.setText(str(tvdb_data["season_count"]))
            self.genres_label.setText(", ".join(tvdb_data["genres"]))

        Thread(target=load_data).start()

    def open_directory(self):
        """
        Opens the currently displayed directory in the system's default file browser
        :return: 
        """
        if sys.platform.startswith("linux"):
            Popen(["xdg-open", self.metadata.path]).wait()
        elif sys.platform == "win32":
            Popen(["explorer", self.metadata.path]).wait()

    def open_tvdb_url(self):
        """
        Opens the TVDB URL in the user's default browser
        :return: 
        """
        webbrowser.open(self.metadata.tvdb_url, new=2)
