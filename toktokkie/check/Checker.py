"""
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

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
"""

import os
from colorama import Fore, Back, Style
from toktokkie.metadata.Metadata import Metadata
from toktokkie.renaming.Renamer import Renamer


class Checker:
    """
    Class that performs checks on Metadata objects
    """

    def __init__(self, metadata: Metadata, show_warnings: bool):
        """
        Initializes the checker
        :param metadata: The metadata to check
        :param show_warnings: Whether or not to show warnings
        """
        self.metadata = metadata
        self.show_warnings = show_warnings

    def check(self):
        """
        Performs sanity checks and prints out anything that's wrong
        :return: None
        """
        print("-" * 80)
        print("Checking {}".format(self.metadata.name))
        self._check_icons()
        self._check_renaming()

    def _check_icons(self):
        """
        Checks that the icon directory exists and there's an icon file for
        every child directory as well as the main directory.
        :return: None
        """
        if not os.path.isdir(self.metadata.icon_directory):
            self.error("Missing icon directory")

        main_icon = os.path.join(self.metadata.icon_directory, "main.png")
        if not os.path.isfile(main_icon):
            self.error("Missing main icon file for {}".format(
                self.metadata.name
            ))

        for child in os.listdir(self.metadata.directory_path):
            child_path = os.path.join(self.metadata.directory_path, child)
            if child.startswith(".") or not os.path.isdir(child_path):
                continue
            else:
                icon_file = os.path.join(
                    self.metadata.icon_directory, child + ".png"
                )
                if not os.path.isfile(icon_file):
                    self.error("Missing icon file for {}".format(child))

    def _check_renaming(self):
        """
        Checks if the renaming of the files and directories of the
        metadata content is correct and up-to-date
        :return: None
        """
        renamer = Renamer(self.metadata)
        for operation in renamer.operations:
            if operation.source != operation.dest:
                self.error("File Mismatch: {}".format(operation))

    # noinspection PyMethodMayBeStatic
    def error(self, text: str):
        """
        Prints a black-on-red error message
        :param text: The text to print
        :return: None
        """
        print("{}{}{}{}".format(Back.RED, Fore.BLACK, text, Style.RESET_ALL))

    def warn(self, text: str):
        """
        Prints a black-on-yellow warning message
        :param text: The text to print
        :return: None
        """
        if self.show_warnings:
            print("{}{}{}{}".format(
                Back.YELLOW, Fore.BLACK, text, Style.RESET_ALL
            ))
