"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from subprocess import Popen


class FileRenamer(object):
    """
    Class that contains static methods to help rename files
    """

    @staticmethod
    def rename_file(file, new_name):
        """
        Renames a file to a new file name, keeping the extension and file path.
        :param file: the file to be renamed
        :param new_name: the new name of the file
        """

        try:
            original_file_name = file.rsplit("/", 1)[1]
        except Exception as e:
            if "list index out of range" in str(e):
                original_file_name = file
            else:
                raise e
        try:
            extension = "." + original_file_name.rsplit(".", 1)[1]
        except Exception as e:
            if "list index out of range" in str(e):
                extension = ""
            else:
                raise e

        new_file = os.path.dirname(file) + "/" + new_name + extension
        Popen(["mv", file, new_file]).wait()
        return new_file
