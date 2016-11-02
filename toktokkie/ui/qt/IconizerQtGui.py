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
from toktokkie.ui.qt.pyuic.iconizer import Ui_IconizerWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog


class IconizerQtGui(QMainWindow, Ui_IconizerWindow):
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

    # noinspection PyArgumentList
    def browse_for_directory(self) -> None:
        """
        Brings up a directory browser window.
        Once a directory was selected, the new directory is then inserted into the
        directory path entry.

        :return: None
        """
        # noinspection PyCallByClass,PyTypeChecker
        directory = QFileDialog.getExistingDirectory(self, "Test")
        if directory:
            self.directory_entry.setText(directory)
