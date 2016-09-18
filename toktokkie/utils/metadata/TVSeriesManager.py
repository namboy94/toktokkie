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


class TVSeriesManager(object):
    """
    Class that handles the metadata for TV Series
    """

    @staticmethod
    def find_recursive_tv_series_directories(directory: str) -> List[str]:
        """
        Finds all directories that include a .meta directory below a given
        directory. Only considers .meta directories with the "tv_series"
        string value in its type file

        In case the given directory does not exist or the current user has no read access,
        an empty list is returned

        :param directory: the directory to check
        :return:          a list of directories that are identified as TV Series
        """
        directories = []

        if not os.path.isdir(directory):
            return []

        try:
            children = os.listdir(directory)
        except PermissionError:
            # If we don't have read permissions for this directory, skip this directory
            return []

        if TVSeriesManager.is_tv_series_directory(directory):
            directories.append(directory)
        else:
            # Parse every subdirectory like the original directory recursively
            for child in children:
                child_path = os.path.join(directory, child)
                if os.path.isdir(child_path):
                    directories += TVSeriesManager.find_recursive_tv_series_directories(child_path)

        return directories

    @staticmethod
    def is_tv_series_directory(directory: str) -> bool:
        """
        Checks if a given directory is a TV Series directory
        A directory is a TV Series directory when it contains a .meta directory and the .meta
        directory contains a file called 'type' which contains the string value 'tv_series'

        :param directory: The directory to check
        :return:          True if the directory is a TV Series directory, False otherwise
        """
        try:
            if ".meta" in os.listdir(directory):
                with open(os.path.join(directory, ".meta", "type")) as typefile:
                    media_type = typefile.read().rstrip().lstrip()
                return media_type == "tv_series"
        except (PermissionError, FileNotFoundError):
            pass

        return False
