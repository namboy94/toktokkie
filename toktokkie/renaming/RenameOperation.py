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


class RenameOperation:
    """
    Class that models a renaming operation
    """

    def __init__(self, source_path: str, dest_path: str):
        """
        Initializes the RenameOperation object
        :param source_path: The currently existing path to the file/directory
        :param dest_path: The new path to the file/directory
        """
        self.source = source_path
        self.dest = dest_path

    def rename(self):
        """
        Renames the episode file to the new name
        :return: None
        """
        self._sanitize()
        os.rename(self.source, self.dest)

    def __str__(self) -> str:
        """
        :return: A string representation of the operation
        """
        return "{} ---> {}".format(self.source, self.dest)

    def _sanitize(self):
        """
        Replaces all illegal file system characters with valid ones.
        Also, limits the length of the resulting file path to 250 characters,
        if at all possible
        :return: The sanitized string
        """
        print(self.dest)
        illegal_characters = {
            "/": "ǁ",
            "\\": "ǁ",
            "?": "‽",
            "<": "←",
            ">": "→",
            ":": "꞉",
            "*": "∗",
            "|": "ǁ",
            "\"": "“"
        }

        sanitized = str(os.path.basename(self.dest))
        for illegal_character, replacement in illegal_characters.items():
            sanitized = sanitized.replace(illegal_character, replacement)

        try:
            name, ext = sanitized.rsplit(".", 1)
            ext = "." + ext
        except (IndexError, ValueError):
            name, ext = [sanitized, ""]

        location = os.path.dirname(self.dest)

        if len(self.dest) > 250 > len(location) + len(ext):
            max_file_length = 250 - (len(location) + len(ext))
            name = name[0:max_file_length]

        self.dest = os.path.join(location, name + ext)