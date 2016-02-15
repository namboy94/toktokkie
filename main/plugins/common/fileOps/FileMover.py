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

from subprocess import Popen


class FileMover(object):
    """
    Class that contains static methods to help move files
    """

    @staticmethod
    def move_file(file, location):
        """
        Moves a file to a new location.
        :param location: the new location of the file
        :param file: the file to be moved
        :return: void
        """

        location_backup = location
        if not location.endswith("/"):
            location_backup += "/"
        file_name = file.rsplit("/", 1)[1]

        new_file = location_backup + file_name

        Popen(["mv", file, new_file]).wait()
        return new_file
