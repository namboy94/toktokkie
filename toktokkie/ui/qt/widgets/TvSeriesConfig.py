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

import os
from typing import List, Dict
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
        self.child_id = "main"

        self.confirm_changes_button.clicked.connect(self.save_data)

        for media_type in MetaDataManager.media_type_map:
            self.media_type_combo_box.addItem(media_type)

    def display_data(self, name: str, tags: List[str], tvdb_url: str or None,
                     audio_langs: List[str], subtitle_langs: List[str],
                     resolutions: List[Dict[str, int]]):
        """
        Displays the editable data of a TvSeriesConfig
        :param name: The name of the series
        :param tags: The tags of the series
        :param tvdb_url: The TVDB URL
        :param audio_langs: The audio languages
        :param subtitle_langs: The subtitle languages
        :param resolutions: The resolutions
        :return: None
        """

        # Derived directly from metadata
        icon_path = os.path.join(self.metadata.path, ".meta/icons/" + self.child_id + ".png")
        self.folder_icon_label.setPixmap(QPixmap(icon_path))
        self.media_type_combo_box.setCurrentIndex(self.media_type_combo_box.findText(self.metadata.type))

        self.series_name_edit.setText(name)
        self.tags_edit.setText(", ".join(tags))
        self.tvdb_url_edit.setText("" if tvdb_url is None else tvdb_url)
        self.audio_language_edit.setText(", ".join(audio_langs))
        self.subtitle_language_edit.setText(", ".join(subtitle_langs))

        for i, widgets in enumerate([
            [self.resolution_one_edit_x, self.resolution_one_edit_y],
            [self.resolution_two_edit_x, self.resolution_two_edit_y],
            [self.resolution_three_edit_x, self.resolution_three_edit_y]
        ]):
            if len(resolutions) > i:
                widgets[0].setText(str(resolutions[i]["x"]))
                widgets[1].setText(str(resolutions[i]["y"]))
            else:
                widgets[0].setText("")
                widgets[1].setText("")

    def set_data(self, metadata: TvSeries, child_id: str):
        """
        Sets the data to be displayed here
        
        :param tv_series: The TvSeries metadata object to be displayed here
        :param child_id: Specifies which subdirectory should be displayed
        
        :return: None
        """
        self.metadata = metadata

    def save_data(self):
        """
        Saves the data currently stored in the UI elements to the info.json file
        :return: None
        """

        self.metadata.name = self.series_name_edit.text()
        self.metadata.type = self.media_type_combo_box.currentText()
        self.metadata.tags = self.tags_edit.text().split(",")
        self.metadata.tvdb_url = self.tvdb_url_edit.text()
        self.metadata.audio_langs = self.audio_language_edit.text().split(",")
        self.metadata.subtitle_langs = self.subtitle_language_edit.text().split(",")

        self.metadata.resolutions = []
        for i, widgets in enumerate([
            [self.resolution_one_edit_x, self.resolution_one_edit_y],
            [self.resolution_two_edit_x, self.resolution_two_edit_y],
            [self.resolution_three_edit_x, self.resolution_three_edit_y]
        ]):
            if widgets[0].text() and widgets[1].text():
                try:
                    self.metadata.resolutions.append({
                        "x": int(widgets[0].text()),
                        "y": int(widgets[1].text())
                    })
                except ValueError:
                    pass

        self.metadata.write_changes()
        self.set_data(self.metadata, self.child_id)


