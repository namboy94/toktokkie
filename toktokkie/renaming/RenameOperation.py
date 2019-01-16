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
        # TODO Take care of illegal characters and character limits
        # Thanks Windows :(
        os.rename(self.source, self.dest)

    def __str__(self) -> str:
        """
        :return: A string representation of the operation
        """
        return "{} ---> {}".format(self.source, self.dest)
