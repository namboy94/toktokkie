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
from threading import Thread
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from xdcc_dl.xdcc.MultipleServerDownloader import MultipleServerDownloader
from toktokkie.utils.iconizing.Iconizer import Iconizer
from toktokkie.utils.renaming.TVSeriesRenamer import TVSeriesRenamer
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager
from toktokkie.utils.iconizing.procedures.ProcedureManager import ProcedureManager
from toktokkie.ui.qt.pyuic.xdcc_download_manager import Ui_XDCCDownloadManagerWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QHeaderView


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

        self.search_results = []
        self.download_queue_list = []

        self.directory_browse_button.clicked.connect(self.browse_for_directory)
        self.download_button.clicked.connect(self.start_download)
        self.search_button.clicked.connect(self.start_search)

        self.add_to_queue_button.clicked.connect(self.add_to_queue)
        self.remove_from_queue_button.clicked.connect(self.remove_from_queue)
        self.move_up_button.clicked.connect(lambda x: self.move_queue_item(up=True))
        self.move_down_button.clicked.connect(lambda x: self.move_queue_item(down=True))

        self.directory_edit.textChanged.connect(self.parse_directory)

        for scheme in SchemeManager.get_scheme_names():
            self.renaming_scheme_combo_box.addItem(scheme)
        for procedure in ProcedureManager.get_procedure_names():
            self.iconizing_method_combo_box.addItem(procedure)
        for pack_searcher in PackSearcher.get_available_pack_searchers() + ["All"]:
            self.search_engine_combo_box.addItem(pack_searcher)

        self.search_result_list.header().setSectionResizeMode(4, QHeaderView.Stretch)

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
        search_engine = self.search_engine_combo_box.currentText()

        if search_engine == "All":
            self.search_results = PackSearcher(PackSearcher.get_available_pack_searchers()).search(search_term)
        else:
            self.search_results = PackSearcher([search_engine]).search(search_term)

        self.search_result_list.clear()
        for i, result in enumerate(self.search_results):
            self.search_result_list.addTopLevelItem(QTreeWidgetItem([str(i),
                                                                     result.get_bot(),
                                                                     str(result.get_packnumber()),
                                                                     str(result.get_size()),
                                                                     result.get_filename()]))

    def start_download(self) -> None:
        """
        Starts the download of each item in the download queue

        :return: None
        """
        if os.path.basename(self.directory_edit.text()) == self.show_name_edit.text():
            destination_directory = self.directory_edit.text()
        else:
            destination_directory = os.path.join(self.directory_edit.text(), self.show_name_edit.text())

        season_directory = os.path.join(destination_directory, "Season " + str(self.season_spin_box.value()))

        progress = Progress(len(self.download_queue_list), callback=self.update_progress_bars)
        packs = list(self.download_queue_list)

        if not MetaDataManager.is_media_directory(destination_directory, "tv_series"):

            dirs = [destination_directory, os.path.join(destination_directory, ".meta", "icons"), season_directory]
            for directory in dirs:
                if not os.path.isdir(directory):
                    os.makedirs(directory)

            with open(os.path.join(destination_directory, ".meta", "type"), 'w') as f:
                f.write("tv_series")

        for i, pack in enumerate(packs):
            name = "xdcc_dl_" + str(i).zfill(int(len(packs) / 10) + 1)
            pack.set_directory(season_directory)
            pack.set_filename(name, override=True)

        def handle_download() -> None:

            MultipleServerDownloader("random", 5).download(packs, progress)

            if self.auto_rename_check.checkState():

                renaming_scheme = SchemeManager.get_scheme_from_scheme_name(
                    self.renaming_scheme_combo_box.currentText())
                renamer = TVSeriesRenamer(destination_directory, renaming_scheme)

                confirmation = renamer.request_confirmation()

                for item in confirmation:
                    if " - S" + str(self.season_spin_box.value()).zfill(2) in item.get_names()[1]:
                        item.confirm()

                renamer.confirm(confirmation)
                renamer.start_rename()

            if self.iconize_check.checkState():
                Iconizer(self.iconizing_method_combo_box.currentText()).iconize_directory(destination_directory)

        Thread(target=handle_download).start()

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

    def refresh_download_queue(self) -> None:
        """
        Refreshes the download queue with the current values in the download queue list

        :return: None
        """
        self.download_queue.clear()
        for pack in self.download_queue_list:
            self.download_queue.addItem(pack.get_filename())
            # TODO Change the displayed name if renaming is active

    def add_to_queue(self) -> None:
        """
        Add the currently selected items in the search result list to the download queue

        :return: None
        """
        for index, row in enumerate(self.search_result_list.selectedIndexes()):
            if index % 5 != 0:
                continue

            self.download_queue_list.append(self.search_results[row.row()])
            self.refresh_download_queue()

        self.search_result_list.clearSelection()

    def remove_from_queue(self) -> None:
        """
        Removes all selected elements from the Download Queue

        :return: None
        """
        for row in reversed(self.download_queue.selectedIndexes()):
            self.download_queue_list.pop(row.row())
        self.refresh_download_queue()

    def move_queue_item(self, up: bool = False, down: bool = False) -> None:
        """
        Moves items on the queue up or down

        :param up:   Pushes the selected elements up
        :param down: Pushes the selected elements down
        :return:     None
        """

        size_check = (lambda x: x > 0) if up and not down else (lambda x: x < len(self.download_queue_list) - 1)
        index_change = (lambda x: x - 1) if up and not down else (lambda x: x + 1)

        indexes = self.download_queue.selectedIndexes() if up and not down \
            else reversed(self.download_queue.selectedIndexes())

        for row in indexes:

            index = row.row()
            if size_check(index):
                self.download_queue_list.insert(index_change(index), self.download_queue_list.pop(index))

        self.refresh_download_queue()

    def update_progress_bars(self, a,b,c,d,e,f,g,h):
        pass