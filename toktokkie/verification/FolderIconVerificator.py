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
from toktokkie.verification.Verificator import Verificator


class FolderIconVerificator(Verificator):
    """
    Verificator that makes sure that folder icons exist for all
    subdirectories in the media directory
    """

    missing_icons = []
    """
    Stores any icons that were identified as missing
    """

    def verify(self) -> bool:
        """
        Checks if all required icon files exist
        :return: True if all icons are present, False if one is missing
        """
        missing = False

        for subdirectory in os.listdir(self.directory.path):

            path = os.path.join(self.directory.path, subdirectory)
            if subdirectory.startswith(".") or not os.path.isdir(path):
                continue

            icon_file = os.path.join(
                self.directory.icon_path,
                subdirectory + ".png"
            )

            if not os.path.isfile(icon_file):
                missing = True
                self.missing_icons.append(icon_file)

        main_icon = os.path.join(self.directory.icon_path, "main.png")

        if not os.path.isfile(main_icon):
            self.missing_icons.append(main_icon)
            missing = True

        return not missing

    def fix(self):
        """
        Allows the user to fix missing icons by saving an icon file
        to the correct location
        :return: None
        """
        for icon_file in self.missing_icons:
            self.print_err("Icon file missing: " + icon_file)
            self.print_ins("Please place an icon file at the above location.")
            resp = self.prompt_yn("Is the icon file at the correct location?")
            while not os.path.isfile(icon_file):
                if resp:
                    self.print_err("No it's not.")
                resp = \
                    self.prompt_yn("Is the icon file at the correct location?")
