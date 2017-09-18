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
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from toktokkie.utils.metadata.media_types.Base import Base
from toktokkie.utils.metadata.media_types.TvSeries import TvSeries


def set_base_series_data(widget: QWidget, metadata: Base, child_id: str) -> None:
    

    

def set_tv_series_data(widget: QWidget, metadata: TvSeries, child_id: str) -> None:
    """
    Sets the data to be displayed in a TvSeriesConfig widget

    :param widget: The widget to fill with the metadata data
    :param metadata: The TvSeries metadata object to be displayed
    :param child_id: Specifies which subdirectory should be displayed

    :return: None
    """

    widget.metadata = metadata
    widget.child_id = child_id

    widget.series_name_edit.setText(metadata.name)
    widget.folder_icon_label.setPixmap(QPixmap(os.path.join(metadata.path, ".meta/icons/" + child_id + ".png")))
    widget.media_type_combo_box.setCurrentIndex(widget.media_type_combo_box.findText(metadata.type))

    widget.tags_edit.setText(", ".join(metadata.tags))
    if metadata.tvdb_url is not None:
        widget.tvdb_url_edit.setText(metadata.tvdb_url)

    widget.audio_language_edit.setText(", ".join(metadata.audio_langs))
    widget.subtitle_language_edit.setText(", ".join(metadata.subtitle_langs))

    if len(metadata.resolutions) > 0:
        widget.resolution_one_edit_x.setText(str(metadata.resolutions[0]["x"]))
        widget.resolution_one_edit_y.setText(str(metadata.resolutions[0]["y"]))
    if len(metadata.resolutions) > 1:
        widget.resolution_two_edit_x.setText(str(metadata.resolutions[1]["x"]))
        widget.resolution_two_edit_y.setText(str(metadata.resolutions[1]["y"]))
    if len(metadata.resolutions) > 2:
        widget.resolution_three_edit_x.setText(str(metadata.resolutions[2]["x"]))
        widget.resolution_three_edit_y.setText(str(metadata.resolutions[2]["y"]))
        
        
def save_tv_series_data(widget: QWidget) -> None:
    """
    Save the TV Series data inside a widget to the metadata info.json file
    
    :param widget: The TvSeriesConfig widget from which to fetch the tv series data
    :return: None
    """
    
    widget.metadata.name = widget.series_name_edit.text()
    widget.metadata.type = widget.media_type_combo_box.currentText()
    widget.metadata.tags = widget.tags_edit.text().split(",")
    widget.metadata.tvdb_url = widget.tvdb_url_edit.text()
    widget.metadata.audio_langs = widget.audio_language_edit.text().split(",")
    widget.metadata.subtitle_langs = widget.subtitle_language_edit.text().split(",")

    widget.metadata.resolutions = []
    for i, widgets in enumerate([
        [widget.resolution_one_edit_x, widget.resolution_one_edit_y],
        [widget.resolution_two_edit_x, widget.resolution_two_edit_y],
        [widget.resolution_three_edit_x, widget.resolution_three_edit_y]
    ]):
        if widgets[0].text() and widgets[1].text():
            try:
                widget.metadata.resolutions.append({
                    "x": int(widgets[0].text()),
                    "y": int(widgets[1].text())
                })
            except ValueError:
                pass

    widget.metadata.write_changes()
    widget.set_data(widget.metadata, widget.child_id)