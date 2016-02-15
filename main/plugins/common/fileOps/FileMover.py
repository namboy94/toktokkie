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

"""
Class that contains static methods to help move files
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class FileMover(object):

    """
    Moves a file to a new location.
    """
    @staticmethod
    def moveFile(file, location):

        locationBackup = location
        if not location.endswith("/"): locationBackup += "/"
        fileName = file.rsplit("/", 1)[1]

        newFile = locationBackup + fileName

        Popen(["mv", file, newFile]).wait()
        return newFile