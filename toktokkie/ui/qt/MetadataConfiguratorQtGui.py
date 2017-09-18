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

# imports
import os
import json
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem
from toktokkie.ui.qt.pyuic.metadata_configurator import Ui_MetadataConfigurator
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager
from toktokkie.ui.qt.widgets.TvSeriesConfig import TvSeriesConfig


class MetadataConfiguratorQtGui(QMainWindow, Ui_MetadataConfigurator):

    def __init__(self, parent: QMainWindow = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.config_file = os.path.join(os.path.expanduser("~"), ".toktokkie/metadata_config.json")
        with open(self.config_file, 'r') as f:
            self.config_data = json.loads(f.read())

        self.media_metadata_items = {}
        self.update_config()

        self.browse_button.clicked.connect(self.browse_for_directory)
        self.add_new_button.clicked.connect(self.add_media_directory)
        self.remove_button.clicked.connect(self.remove_media_directory)
        self.media_tree.currentItemChanged.connect(self.load_widget_data)

        self.media_type_widgets = {
            "tv_series": TvSeriesConfig(self)
        }

        for widget_type in self.media_type_widgets:
            self.widget_stack.addWidget(self.media_type_widgets[widget_type])

        # TODO implement widgets for others
        self.media_type_widgets["anime_series"] = self.media_type_widgets["tv_series"]

    def parse_media_directories(self):
        self.media_metadata_items = {}
        for directory in self.config_data["media_directories"]:

            if not os.path.isdir(directory):
                continue

            for item in sorted(os.listdir(directory)):
                metadata = MetaDataManager.autoresolve_directory(os.path.join(directory, item))
                if metadata is not None:
                    self.media_metadata_items[item] = metadata

        self.media_tree.clear()
        for key, item in self.media_metadata_items.items():
            widget = QTreeWidgetItem([key])
            for child in item.get_child_names():
                widget.addChild(QTreeWidgetItem([child]))
            self.media_tree.addTopLevelItem(widget)

    def browse_for_directory(self) -> None:
        """
        Brings up a directory browser window.
        Once a directory was selected, the new directory is then inserted into the
        directory path entry.

        :return: None
        """
        directory = QFileDialog.getExistingDirectory(self, "Browse")
        if directory:
            self.add_new_edit.setText(directory)

    def add_media_directory(self) -> None:
        entry = self.add_new_edit.text()
        if entry:
            self.config_data["media_directories"].append(entry)
            self.update_config()

    def remove_media_directory(self) -> None:
        selected = self.media_directory_list.selectedItems()
        for item in selected:
            self.config_data["media_directories"].remove(item.data(0, 0))
        self.update_config()

    def update_config(self) -> None:
        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self.config_data))
        self.media_directory_list.clear()
        for directory in self.config_data["media_directories"]:
            self.media_directory_list.addTopLevelItem(QTreeWidgetItem([directory]))
        self.parse_media_directories()

    def load_widget_data(self, widget: QTreeWidgetItem) -> None:

        if widget.parent() is None:
            metadata = self.media_metadata_items[widget.data(0, 0)]
            widget = self.media_type_widgets[metadata.type]
            widget.set_data(metadata)
            self.widget_stack.setCurrentWidget(widget)

        else:
            metadata = self.media_metadata_items[widget.parent().data(0, 0)]
            widget = self.media_type_widgets[metadata.type]
            widget.set_data(metadata, widget.data(0, 0))
            self.widget_stack.setCurrentWidget(widget)
