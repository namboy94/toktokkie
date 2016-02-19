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


class Installer(object):
    """
    Class that handles installation of the program
    """

    def __init__(self):
        """
        Constructor
        :return: void
        """
        self.main_dir = os.getenv("HOME") + "/.mediamanager"
        self.config_dir = self.main_dir + "/configs"
        self.mainConfig = self.config_dir + "/mainconfig"

    def is_installed(self):
        """
        Checks if the program is installed
        :return: True is it is installed, False if not
        """
        if not os.path.isdir(self.main_dir) or \
                not os.path.isdir(self.config_dir) or \
                not os.path.isfile(self.mainConfig):
            return False
        return True

    def install(self):
        """
        Installs the program
        :return: void
        """
        if not os.path.isdir(self.main_dir):
            Popen(["mkdir", self.main_dir]).wait()
        if not os.path.isdir(self.config_dir):
            Popen(["mkdir", self.config_dir]).wait()
        if not os.path.isfile(self.mainConfig):
            self.__write_main_config__()

    def __write_main_config__(self):
        """
        Writes a default config file
        :return: void
        """
        Popen(["touch", self.mainConfig])
        file = open(self.mainConfig, "w")
        file.write("[plugins]\n")
        file.write("renamer = True\n")
        file.write("batch-download\n")
        file.write("iconizer = True\n")
        file.write("\n[defaults]\n")
        file.write("downloader = hexchat\n#options = (twisted|hexchat)\n")
        file.close()