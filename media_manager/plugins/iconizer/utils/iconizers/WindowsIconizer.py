"""
LICENSE:

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

LICENSE
"""

import os
from subprocess import Popen


class WindowsIconizer(object):
    """
    Class that iconizes folders in Windows Explorer
    """

    @staticmethod
    def iconize(directory, icon):
        """
        Iconizes the folder
        :param icon: the icon to be used
        :param directory: the directory to be iconized
        :return: void
        """
        desktop_ini_file = os.path.join(directory, "desktop.ini")
        relative_path = os.path.relpath(icon, directory)
        if os.path.isfile(desktop_ini_file):
            Popen(["attrib", "-s", "-h", "-r", desktop_ini_file]).wait()
        file = open(desktop_ini_file, 'w')
        file.writelines(["[.ShellClassInfo]",
                         "IconFile=" + relative_path,
                         "IconIndex=0",
                         "[ViewState]",
                         "Mode=",
                         "Vid=",
                         "FolderType=Videos"])

        Popen(["attrib", "+s", "+h", "+r", desktop_ini_file]).wait()
        Popen(["attrib", "+r", directory]).wait()
