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
from copy import copy
from subprocess import Popen
from threading import Thread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from toktokkie.utils.metadata.media_types import Base
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager


class GenericConfig(QWidget):
    """
    A class with common methods shared between all Config Widgets
    """

    def initialize(self):
        """
        Initializes common buttons and combo boxes
        :return: None
        """
        self.confirm_changes_button.clicked.connect(self.save_data)
        self.open_directory_button.clicked.connect(self.open_directory)
        for media_type in MetaDataManager.media_type_map:
            self.media_type_combo_box.addItem(media_type)
    
    def set_metadata(self, metadata: Base, child_key: str):
        """
        Sets the metadata of the Config widget
        :param metadata: The metadata to set 
        :param child_key: The child key for use with media types that allow child elements
        :return: None
        """
        # noinspection PyAttributeOutsideInit
        self.metadata = copy(metadata)

        if self.metadata in ["tv_series", "anime_series"] and child_key != "main":
            self.metadata.set_child_extender("seasons", child_key)

        self.display()
    
    def save_data(self):
        """
        Saves the data in the UI elements to the info.json file
        :return: None
        """
        {
            "base": store_base_info,
            "tv_series": store_tv_series_info,
            "anime_series": store_anime_series_info
        }[self.metadata.media_type](self)
        self.metadata.write_changes()
        self.display()
    
    def display(self):
        """
        Displays the information in the info.json file
        :return: None
        """
        {
            "base": display_base_info,
            "tv_series": display_tv_series_info,
            "anime_series": display_anime_series_info
        }[self.metadata.media_type](self)
        Thread(target=self.load_online_data).start()

    def load_online_data(self):
        """
        Method that is called asynchronously to load online data
        :return: None
        """
        pass
        
    def open_directory(self):
        """
        Opens the currently displayed directory in the system's default file browser
        :return: None
        """
        if sys.platform.startswith("linux"):
            Popen(["xdg-open", self.metadata.path]).wait()
        elif sys.platform == "win32":
            Popen(["explorer", self.metadata.path]).wait()


def display_base_info(widget: GenericConfig):
    """
    Displays the information in a Base metadata object
    Also kicks of the load_online_data method
    
    :param widget: The widget in which to display the information 
    :return: None
    """
    widget.media_type_combo_box.setCurrentIndex(widget.media_type_combo_box.findText(widget.metadata.media_type))
    widget.series_name_edit.setText(widget.metadata.name)
    widget.folder_icon_label.setPixmap(QPixmap(widget.metadata.get_icon_path()))
    widget.tags_edit.setText(", ".join(widget.metadata.tags))
    

def display_tv_series_info(widget: GenericConfig):
    """
    Displays the information in a TvSeries metadata object
    
    :param widget: The widget in which to display the information 
    :return: None
    """
    display_base_info(widget)
    
    widget.tvdb_url_edit.setText(widget.metadata.tvdb_url)
    widget.audio_language_edit.setText(", ".join(widget.metadata.audio_langs))
    widget.subtitle_language_edit.setText(", ".join(widget.metadata.subtitle_langs))

    for i, widgets in enumerate([
        [widget.resolution_one_edit_x, widget.resolution_one_edit_y],
        [widget.resolution_two_edit_x, widget.resolution_two_edit_y],
        [widget.resolution_three_edit_x, widget.resolution_three_edit_y]
    ]):
        if len(widget.metadata.resolutions) > i:
            widgets[0].setText(str(widget.metadata.resolutions[i]["x"]))
            widgets[1].setText(str(widget.metadata.resolutions[i]["y"]))
        else:
            widgets[0].setText("")
            widgets[1].setText("")


def display_anime_series_info(widget: GenericConfig):
    """
    Displays the information in a AnimeSeries metadata object

    :param widget: The widget in which to display the information 
    :return: None
    """
    display_tv_series_info(widget)
    widget.myanimelist_url_edit.setText(widget.metadata.myanimelist_url)


def store_base_info(widget: GenericConfig):
    """
    Stores the Base metadata info from the UI elements into the metadata object
    :param widget: The widget from which to retrieve the data
    :return: None
    """
    widget.metadata.name = widget.series_name_edit.text()
    widget.metadata.media_type = widget.media_type_combo_box.currentText()
    widget.metadata.tags = widget.tags_edit.text().split(",")


def store_tv_series_info(widget: GenericConfig):
    """
    Stores the TvSeries metadata info from the UI elements into the metadata object
    :param widget: The widget from which to retrieve the data
    :return: None
    """
    store_base_info(widget)
    
    widget.metadata.tvdb_url = widget.tvdb_url_edit.text()
    widget.metadata.audio_langs = widget.audio_language_edit.text().split(",")
    widget.metadata.subtitle_langs = widget.subtitle_language_edit.text().split(",")

    resolutions = []
    for i, widgets in enumerate([
        [widget.resolution_one_edit_x, widget.resolution_one_edit_y],
        [widget.resolution_two_edit_x, widget.resolution_two_edit_y],
        [widget.resolution_three_edit_x, widget.resolution_three_edit_y]
    ]):
        if widgets[0].text() and widgets[1].text():
            try:
                resolutions.append({
                    "x": int(widgets[0].text()),
                    "y": int(widgets[1].text())
                })
            except ValueError:
                pass
    widget.metadata.resolutions = resolutions  # Must be set here due to the setter method


def store_anime_series_info(widget: GenericConfig):
    """
    Stores the AnimeSeries metadata info from the UI elements into the metadata object
    :param widget: The widget from which to retrieve the data
    :return: None
    """
    store_tv_series_info(widget)
    widget.metadata.myanimelist_url = widget.myanimelist_url_edit.text()
