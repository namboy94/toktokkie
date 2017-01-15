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
import sys
import time
import random
from threading import Thread
from PyQt5.QtCore import pyqtSignal
from toktokkie.utils.renaming.TVSeriesRenamer import TVSeriesRenamer
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager
from toktokkie.ui.qt.pyuic.tv_series_renamer import Ui_TVSeriesRenamer
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QHeaderView, QPushButton, QMessageBox


class TVSeriesRenamerQtGui(QMainWindow, Ui_TVSeriesRenamer):
    """
    Class that models th QT GUI for the TV Series Renamer
    """

    spinner_updater_signal = pyqtSignal(str, QPushButton, name="spinner_updater")
    visibility_switcher_signal = pyqtSignal(bool, name="visibility_switcher")
    populate_list_signal = pyqtSignal(str, name="populate_list")

    def __init__(self, parent: QMainWindow = None) -> None:
        """
        Sets up the interactive UI elements

        :param parent: the parent window
        """
        super().__init__(parent)
        self.setupUi(self)

        # Initialize UI elements
        self.browse_button.clicked.connect(self.browse_for_directory)
        self.directory_entry.textChanged.connect(self.parse_directory)
        self.cancel_button.clicked.connect(self.cancel)
        self.confirm_button.clicked.connect(self.confirm)
        self.rename_list.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.selection_remover_button.clicked.connect(self.remove_selection)
        self.recursive_check.stateChanged.connect(self.parse_directory)

        self.spinner_updater_signal.connect(self.update_spinner_text)
        self.visibility_switcher_signal.connect(lambda x: self.meta_warning_label.setVisible(x))  # pragma: no cover
        self.populate_list_signal.connect(self.populate_list)

        for scheme in SchemeManager.get_scheme_names():
            self.scheme_selector.addItem(scheme)

        # Local Variables
        self.confirmation = []
        self.renamer = None
        self.parser_id = 0

        self.parser_thread = None

        self.renaming = False
        self.parsing = False
        self.populating = False

    # noinspection PyArgumentList
    def browse_for_directory(self) -> None:
        """
        Brings up a directory browser window.
        Once a directory was selected, the new directory is then inserted into the
        directory path entry.

        :return: None
        """

        if not self.renaming and not self.parsing:  # pragma: no cover

            # noinspection PyCallByClass
            directory = QFileDialog.getExistingDirectory(self, "Browse")
            if directory:
                self.directory_entry.setText(directory)

    def parse_directory(self) -> None:
        """
        Checks the currently entered directory for episode files to rename.
        All discovered episodes are then displayed in the rename list

        This can be cancelled using the cancel button, which is why the thread is assigned a random 50-character
        id with which can be determined if the thread was cancelled

        :return: None
        """
        if self.renaming or self.parsing:
            return

        self.cancel()
        self.parsing = True

        def parse():

            parse_id = random.randint(int(50 * "1"), int(51 * "1"))
            self.parser_id = parse_id

            self.start_spinner("parse")
            directory = self.directory_entry.text()
            while directory.endswith(os.path.sep):
                directory = directory.rsplit(os.path.sep, 1)[0]

            if os.path.isdir(directory) and \
                    (MetaDataManager.is_media_directory(directory, media_type="tv_series") or
                     self.recursive_check.checkState()):

                renaming_scheme = self.scheme_selector.currentText()
                renaming_scheme = SchemeManager.get_scheme_from_scheme_name(renaming_scheme)

                renamer = TVSeriesRenamer(directory, renaming_scheme, self.recursive_check.checkState())
                confirmation = renamer.request_confirmation()

                if parse_id == self.parser_id:

                    self.visibility_switcher_signal.emit(False)
                    self.renamer = renamer
                    self.confirmation = confirmation
                    self.populate_list_signal.emit("")

                    while self.populating:  # pragma: no cover
                        pass

                    self.parsing = False
            else:
                self.parsing = False

        self.parser_thread = Thread(target=parse)
        self.parser_thread.start()

    # noinspection PyUnusedLocal
    def populate_list(self, arg: str = None) -> None:
        """
        Populates the Tree Widget with a list of episode's new and old names

        :param arg: Mandatory passed argument
        :return:    None
        """
        self.populating = True
        for item in self.confirmation:
            self.rename_list.addTopLevelItem(QTreeWidgetItem([item.get_names()[0], item.get_names()[1]]))
        self.populating = False

    def cancel(self) -> None:
        """
        Cancels the current Renaming process and resets the UI

        :return: None
        """

        if self.renaming:
            return

        self.renamer = None
        self.rename_list.clear()
        self.meta_warning_label.setVisible(True)
        self.parser_id = 0
        self.parsing = False

    def confirm(self) -> None:
        """
        Starts the renaming process

        :return: None
        """
        if self.renaming or self.renamer is None:
            return

        self.renaming = True

        def rename():

            self.start_spinner("rename")

            for item in self.confirmation:
                item.confirmed = True

            self.renamer.confirm(self.confirmation)
            self.renamer.start_rename()
            self.renaming = False
            self.directory_entry.textChanged.emit("")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Complete")
            msg.setText("The files where successfully renamed")
            msg.setStandardButtons(QMessageBox.Ok)

            if not sys.argv == [sys.argv[0], "-platform", "minimal"]:  # pragma: no cover
                msg.exec_()

        Thread(target=rename).start()

    def remove_selection(self) -> None:
        """
        Removes the selected items from the list

        :return: None
        """
        for index, row in enumerate(self.rename_list.selectedIndexes()):
            if index % 2 != 0:
                continue
            self.confirmation.pop(row.row() - int(index / 2))
        self.rename_list.clear()
        for item in self.confirmation:
            self.rename_list.addTopLevelItem(QTreeWidgetItem([item.get_names()[0], item.get_names()[1]]))

    def start_spinner(self, mode: str) -> None:
        """
        Starts a small animation while something is loading, parsing etc.

        :param mode:  The mode determines which UI element is going to be 'spun'
        :return:      None
        """
        renaming = mode == "rename"
        parsing = mode == "parse"

        def spin():

            while (renaming and self.renaming) or (parsing and self.parsing):

                if renaming and self.renaming:
                    new_text = "Renaming" + (self.confirm_button.text().count(".") % 3 + 1) * "."
                    self.spinner_updater_signal.emit(new_text, self.confirm_button)

                if parsing and self.parsing:
                    new_text = "Reloading" + (self.browse_button.text().count(".") % 3 + 1) * "."
                    self.spinner_updater_signal.emit(new_text, self.browse_button)
                time.sleep(0.3)

            if renaming and not self.renaming:
                self.spinner_updater_signal.emit("Confirm", self.confirm_button)
            if parsing and not self.parsing:
                self.spinner_updater_signal.emit("Browse", self.browse_button)

        Thread(target=spin).start()

    # noinspection PyMethodMayBeStatic
    def update_spinner_text(self, text: str, button: QPushButton) -> None:
        """
        Updates the text on a button, to be used by a spinner thread

        :param text:   The new text to be displayed
        :param button: The button whose text will be changed
        :return:       None
        """
        button.setText(text)

    def closeEvent(self, event: object) -> None:
        """
        Clean up variables that could keep threads from terminating

        :return: None
        """
        self.renaming = False
        self.parsing = False
        self.populating = False
