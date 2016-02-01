"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a progam that allows convenient managing of various
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

"""
Class that contains static methods to help rename files
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class FileRenamer(object):

    """
    Renames a file to a new file name, keeping the extension and filepath.
    """
    @staticmethod
    def renameFile(file, newname):

        try:
            originalFileName = file.rsplit("/", 1)[1]
        except Exception as e:
            if "list index out of range" in str(e):
                originalFileName = file
            else:
                raise e
        try:
            extension = "." + originalFileName.rsplit(".", 1)[1]
        except Exception as e:
            if "list index out of range" in str(e):
                extension = ""
            else:
                raise e

        newFile = os.path.dirname(file) + "/" + newname + extension
        Popen(["mv", file, newFile]).wait()
        return newFile