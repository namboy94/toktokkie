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
from toktokkie.ui.qt.pyuic.tv_series_renamer import Ui_Renamer
from toktokkie.utils.renaming.TVSeriesRenamer import TVSeriesRenamer
from toktokkie.utils.metadata.TVSeriesManager import TVSeriesManager
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTreeWidgetItem, QHeaderView


class TVSeriesRenamerQtGui(QMainWindow, Ui_Renamer):
    """
    Class that models th QT GUI for the TV Series Renamer
    """

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
        self.cancel_button.clicked.connect(lambda: self.cancel(True))
        self.confirm_button.clicked.connect(self.confirm)
        self.rename_list.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.selection_inverter_button.clicked.connect(self.invert_selection)
        self.selection_remover_button.clicked.connect(self.remove_selection)

        for scheme in SchemeManager.get_scheme_names():
            self.scheme_selector.addItem(scheme)

        # Local Variables
        self.confirmation = []
        self.renamer = None

    def browse_for_directory(self) -> None:
        """
        Brings up a directory browser window.
        Once a directory was selected, the new directory is then inserted into the
        directory path entry.

        :return: None
        """
        # TODO check if supression necessary
        # noinspection PyCallByClass
        directory = QFileDialog.getExistingDirectory(self, "Test")
        if directory:
            self.directory_entry.setText(directory)

    def parse_directory(self) -> None:
        """
        Checks the currently entered directory for episode files to rename.
        All discovered episodes are then displayed in the rename list

        :return: None
        """
        self.cancel(False)
        directory = self.directory_entry.text()

        if os.path.isdir(directory) and TVSeriesManager.is_tv_series_directory(directory):

            self.meta_warning_label.setVisible(False)

            renaming_scheme = self.scheme_selector.currentText()
            renaming_scheme = SchemeManager.get_scheme_from_scheme_name(renaming_scheme)
            self.renamer = TVSeriesRenamer(directory, renaming_scheme, False)

            self.confirmation = self.renamer.request_confirmation()

            for item in self.confirmation:
                self.rename_list.addTopLevelItem(QTreeWidgetItem([item.get_names()[0], item.get_names()[1]]))

    def cancel(self, directory_entry: bool = True) -> None:
        """
        Cancels the current Renaming process and resets the UI

        :param directory_entry: Clearing the directory entry can be disabled optionally
        :return: None
        """
        self.confirmation = []
        self.renamer = None
        self.rename_list.clear()
        self.meta_warning_label.setVisible(True)
        if directory_entry:
            self.directory_entry.clear()

    def confirm(self) -> None:
        """
        Starts the renaming process

        :return: None
        """
        for item in self.confirmation:
            item.confirmed = True

        self.renamer.confirm(self.confirmation)
        self.renamer.start_rename()
        self.parse_directory()

    def invert_selection(self) -> None:
        """
        Inverts the current selection of list elements

        :return: None
        """
        pass

    def remove_selection(self) -> None:
        """
        Removes the selected items from the list

        :return: None
        """
        print(self.rename_list.selectedItems())
        print(self.rename_list.selectedIndexes())


def start_gui():
    app = QApplication(sys.argv)
    form = TVSeriesRenamerQtGui()
    form.show()
    app.exec_()

if __name__ == '__main__':
    start_gui()

