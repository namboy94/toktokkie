"""LICENSE
Copyright 2019 Hermann Krumrey <hermann@krumreyh.com>

This file is part of toktokkie.

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
LICENSE"""

from PyQt5.QtWidgets import QDialog, QMainWindow, QListWidgetItem
from toktokkie.gui.pyuic.remove_directory_dialog import \
    Ui_RemoveDirectoryDialog


class RemoveDirectoryDialog(QDialog, Ui_RemoveDirectoryDialog):
    """
    Class that models a dialog that allows a user to remove a directory
    from the config file
    """

    def __init__(self, parent: QMainWindow):
        """
        Initializes the widget
        :param parent: The parent window
        """
        super().__init__(parent)
        self.setupUi(self)
        self.remove_button.clicked.connect(self.remove_selected)
        media_dirs = self.parent().config["media_directories"]

        for path in media_dirs:
            self.directory_list.addItem(QListWidgetItem(path))

    def remove_selected(self):
        """
        Removes the selected directories from the config and
        closes the dialog afterwards
        :return: None
        """
        selected = self.directory_list.selectedItems()
        for item in selected:
            self.parent().config["media_directories"].remove(item.text())
        self.parent().write_config()
        self.parent().reload()

        self.close()
