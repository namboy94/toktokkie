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
from toktokkie.ui.qt.pyuic.iconizer import Ui_FolderIconizerWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog


class IconizerQtGui(QMainWindow, Ui_FolderIconizerWindow):


    def __init__(self, parent: QMainWindow = None) -> None:

        super().__init__(parent)
        self.setupUi(self)

    # noinspection PyArgumentList
    def browse_for_directory(self) -> None:

        # noinspection PyCallByClass,PyTypeChecker
        directory = QFileDialog.getExistingDirectory(self, "Browse")
        if directory:
            self.directory_entry.setText(directory)
