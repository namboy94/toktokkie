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
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager
from toktokkie.ui.qt.pyuic.xdcc_download_manager import Ui_XDCCDownloadManagerWindow
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager
from toktokkie.utils.iconizing.procedures.ProcedureManager import ProcedureManager


class XDCCDownloadManagerQtGui(QMainWindow, Ui_XDCCDownloadManagerWindow):
    """
    Class that defines the functionality of the Folder Iconizer GUI
    """

    def __init__(self, parent: QMainWindow = None) -> None:
        """
        Initializes the interactive components of the GUI

        :param parent: The parent QT GUI
        """
        super().__init__(parent)
        self.setupUi(self)

        self.directory_browse_button.clicked.connect(self.browse_for_directory)
        self.download_button.clicked.connect(self.start_download)
        self.search_button.clicked.connect(self.start_search)

        self.add_to_queue_button.clicked.connect(self.add_to_queue)
        self.remove_from_queue_button.clicked.connect(self.remove_from_queue)
        self.move_up_button.clicked.connect(self.move_up)
        self.move_down_button.clicked.connect(self.move_down)

        self.directory_edit.textChanged.connect(self.parse_directory)

        for scheme in SchemeManager.get_scheme_names():
            self.renaming_scheme_combo_box.addItem(scheme)
        for procedure in ProcedureManager.get_procedure_names():
            self.iconizing_method_combo_box.addItem(procedure)
        for pack_searcher in PackSearcher.get_available_pack_searchers():
            self.search_engine_combo_box.addItem(pack_searcher)

    def browse_for_directory(self) -> None:
        """
        Lets the user browse for a local directory path

        :return: None
        """
        # noinspection PyCallByClass,PyTypeChecker, PyArgumentList
        directory = QFileDialog.getExistingDirectory(self, "Browse")
        if directory:
            self.directory_edit.setText(directory)

    def start_search(self) -> None:
        """
        Starts the search using the

        :return: None
        """
        search_term = self.search_term_edit.text()
        search_engine = "?"

        # Search and Fill List
        # Clear Download Queue

    def start_download(self) -> None:
        """
        Starts the download of each item in the download queue

        :return: None
        """
        destination_directory = self.directory_edit.text()
        # Get selected items

        # Check if .meta exists, if not, create it, tv_show

        # Download, keep progress bar informed though

        # Iconize

    def parse_directory(self) -> None:
        """
        Parses the currently entered directory, checks if it contains a .meta directory.
        Fills show name, episode and season according to info found.
        Search Term = show name

        :return: None
        """
        directory = self.directory_edit.text()

        if MetaDataManager.is_media_directory(directory):
            # TODO Season, Episode
            self.episode_spin_box.setValue(1)
            self.season_spin_box.setValue(1)

        else:
            self.episode_spin_box.setValue(1)
            self.season_spin_box.setValue(1)

        name = os.path.basename(directory)
        self.search_term_edit.setText(name)
        self.show_name_edit.setText(name)

    def add_to_queue(self) -> None:
        pass

    def remove_from_queue(self) -> None:
        pass

    def move_up(self) -> None:
        pass

    def move_down(self) -> None:
        pass
