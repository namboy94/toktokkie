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
import json
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from toktokkie.utils.xdcc.updating.JsonHandler import JsonHandler
from toktokkie.utils.xdcc.updating.AutoSearcher import AutoSearcher
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager
from toktokkie.ui.qt.pyuic.xdcc_update_configurator import Ui_XDCCUpdateConfiguratorWindow


class XDCCUpdateConfiguratorQtGui(QMainWindow, Ui_XDCCUpdateConfiguratorWindow):
    """
    Class that defines the functionality of the XDCC Updater GUI
    """

    def __init__(self, parent: QMainWindow = None) -> None:
        """
        Initializes the interactive components of the GUI

        :param parent: The parent QT GUI
        """
        super().__init__(parent)
        self.setupUi(self)

        self.file_loaded = False

        for naming_scheme in SchemeManager.get_scheme_names():
            self.naming_scheme_combo_box.addItem(naming_scheme)
        for pattern in AutoSearcher.get_available_patterns():
            self.pattern_combo_box.addItem(pattern)
        for searcher in PackSearcher.get_available_pack_searchers():
            self.search_engine_combo_box.addItem(searcher)

        self.load_button.clicked.connect(self.browse_for_json_file)
        self.series_list.selectionModel().selectionChanged.connect(self.load_selected_series)

        self.json_handler = None
        self.series = []

    def browse_for_json_file(self) -> None:
        """
        Lets the user browse for the JSON file containing the updater configuration

        :return: None
        """
        # noinspection PyCallByClass,PyTypeChecker, PyArgumentList
        selected = QFileDialog.getOpenFileName(self, "Browse")
        if selected[0]:
            try:
                self.json_handler = JsonHandler(selected[0])
                self.file_loaded = True
                self.populate_series_list()
            except json.decoder.JSONDecodeError:
                pass  # TODO Let user know he's a dumm-dumm

    def populate_series_list(self) -> None:
        """
        Populates the series list with the series loaded from the JSON file

        :return: None
        """
        self.series_list.clear()
        self.series = self.json_handler.get_series()

        for series in self.series:
            self.series_list.addItem(series.get_search_name())

    def load_selected_series(self) -> None:
        """
        Loads the selected series from the series list

        :return: None
        """
        selected_series = self.series[self.series_list.selectedIndexes()[0].row()]

        self.directory_edit.setText(selected_series.get_destination_directory())
        self.search_name_edit.setText(selected_series.get_search_name())

        self.quality_combo_box.setCurrentIndex(
            self.quality_combo_box.findText(selected_series.get_quality_identifier()))

        self.bot_edit.setText(selected_series.get_bot_preference())
        self.season_spin_box.setValue(selected_series.get_season())

        self.search_engine_combo_box.setCurrentIndex(
            self.search_engine_combo_box.findText(selected_series.get_search_engines()[0]))

        self.naming_scheme_combo_box.setCurrentIndex(
            self.naming_scheme_combo_box.findText(selected_series.get_naming_scheme()))

        self.pattern_combo_box.setCurrentIndex(
            self.pattern_combo_box.findText(selected_series.get_search_pattern()))
