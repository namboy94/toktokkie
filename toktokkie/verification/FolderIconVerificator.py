"""LICENSE
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
LICENSE"""

import os
from typing import List
from toktokkie.verification.Verificator import Verificator


class FolderIconVerificator(Verificator):
    """
    Verificator that makes sure that folder icons exist for all
    subdirectories in the media directory
    """

    def verify(self) -> bool:
        """
        Checks if all required icon files exist
        :return: True if all icons are present, False if one is missing
        """
        missing_icons = self.__get_missing_icons()
        return len(missing_icons) <= 0

    def fix(self):
        """
        Allows the user to fix missing icons by saving an icon file
        to the correct location
        :return: None
        """
        for icon_file in self.__get_missing_icons():
            self.prompt_until_verified(
                "Icon file missing: " + icon_file,
                "Please place an icon file at the above location.",
                "Is the icon file at the correct location?",
                "No it's not.",
                lambda: os.path.isfile(icon_file)
            )

    def __get_missing_icons(self) -> List[str]:
        """
        Checks for missing icons and returns the paths at
        which they are expected to be
        :return: The list of icon file paths
        """
        missing_icons = []

        for subdirectory in os.listdir(self.directory.path):

            path = os.path.join(self.directory.path, subdirectory)
            if subdirectory.startswith(".") or not os.path.isdir(path):
                print("", end="")  # Somehow, coverage is broken without this
                continue

            icon_file = os.path.join(
                self.directory.icon_path,
                subdirectory + ".png"
            )

            if not os.path.isfile(icon_file):
                missing_icons.append(icon_file)

        main_icon = os.path.join(self.directory.icon_path, "main.png")

        if not os.path.isfile(main_icon):
            missing_icons.append(main_icon)

        return missing_icons
