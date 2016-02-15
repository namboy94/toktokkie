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
import sys
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
        self.mainDir = os.getenv("HOME") + "/.mediamanager"
        self.configDir = self.mainDir + "/configs"
        self.scriptDir = self.mainDir + "/scripts"
        self.mainConfig = self.configDir + "/mainconfig"
        self.xdccDLScript = self.scriptDir + "/xdccbot.py"
        self.programDir = self.mainDir + "/program"
        self.executable = "/usr/bin/mmgui"

    def is_installed(self):
        """
        Checks if the program is installed
        :return: True is it is installed, False if not
        """
        if not os.path.isdir(self.mainDir) or \
                not os.path.isdir(self.configDir) or \
                not os.path.isdir(self.scriptDir) or \
                not os.path.isfile(self.mainConfig) or \
                not os.path.isfile(self.xdccDLScript) or \
                not os.path.isdir(self.programDir) or \
                not os.path.isfile(self.executable):
            return False
        return True

    def install(self):
        """
        Installs the program
        :return: void
        """
        if not os.path.isdir(self.mainDir):
            Popen(["mkdir", self.mainDir]).wait()
        if not os.path.isdir(self.configDir):
            Popen(["mkdir", self.configDir]).wait()
        if not os.path.isdir(self.scriptDir):
            Popen(["mkdir", self.scriptDir]).wait()
        if not os.path.isfile(self.mainConfig):
            self.__write_main_config__()
        if not os.path.isfile(self.xdccDLScript):
            self.__copy_xdcc_script_file__()
        if not os.path.isdir(self.programDir):
            Popen(["cp", "-rf", Installer.__get_source_dir__(), self.programDir]).wait()
        if not os.path.isfile(self.executable):
            Popen(["sudo", "cp", Installer.__get_source_dir__() + "/main/startup/scripts/mediamanagergui.sh",
                   self.executable]).wait()
            Popen(["sudo", "chmod", "755", self.executable]).wait()

    def __write_main_config__(self):
        """
        Writes a default config file
        :return: void
        """
        Popen(["touch", self.mainConfig])
        file = open(self.mainConfig, "w")
        file.write("[plugins]\n")
        file.write("renamer = True\n")
        file.write("xdcc-searchdownload = True\n")
        file.write("\n[defaults]\n")
        file.write("downloader = twisted\n#options = (twisted|hexchat)\n")
        file.close()

    def __copy_xdcc_script_file__(self):
        """
        Copies the xdcc download script to the program directory.
        THis has to be done differently once twisted's irc module is ported to python 3
        :return: void
        """
        original = os.path.dirname(sys.argv[0]) + "/external/xdccbot.py"
        Popen(["cp", original, self.xdccDLScript]).wait()

    @staticmethod
    def __get_source_dir__():
        """
        Gets the source directory of the python program running
        :return: the source directory
        """
        directory = os.path.dirname(sys.argv[0])
        return str(os.path.abspath(directory).rsplit("/", 1)[0])
