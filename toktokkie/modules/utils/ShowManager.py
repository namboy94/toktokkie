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
from typing import List


class ShowManager(object):
    """
    Class that handles the Show Manager methods
    """

    @staticmethod
    def find_recursive_show_directories(directory: str) -> List[str]:
        """
        Finds all directories that include a .meta directory below a given
        directory.

        :param directory: the directory to check
        :return: a list of directories that include .meta directories
        """
        directories = []

        # Check if the directory is a valid directory
        if not os.path.isdir(directory):
            raise NotADirectoryError("Not a directory")

        # List the directory's subdirectories
        try:
            children = os.listdir(directory)
        except PermissionError:
            # If we don't have read permissions for this directory, skip this directory
            return []

        # Check if one of the subdirectories is .meta
        if ".meta" in children:
            # If yes, add the directory
            directories.append(directory)
        else:
            # Else parse every subdirectory like the original directory recursively
            for child in children:
                child_path = os.path.join(directory, child)
                if os.path.isdir(child_path):
                    directories += ShowManager.find_recursive_show_directories(child_path)

        return directories
