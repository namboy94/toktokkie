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
import sys
from subprocess import Popen
from toktokkie.utils.iconizing.procedures.GenericProcedure import GenericProcedure


class DesktopIniProcedure(GenericProcedure):
    """
    Class that models a Windows Explorer Desktop.ini-based iconizer
    """

    @staticmethod
    def is_applicable() -> bool:
        """
        The Desktop.ini iconizer is applicable if the system is running Windows

        :return: True if the iconizer is applicable to the system, False otherwise
        """
        return sys.platform == "win32"

    @staticmethod
    def iconize(directory: str, icon_file: str) -> None:
        """
        Iconizes the given directory using hidden desktop.ini files with metadata.
        The icon file must be a .ico file, but the file extension may be omitted (e.g. icon instead of icon.ico)

        :param directory: The directory to iconize
        :param icon_file: The icon file to use
        :return:          None
        """
        # NOTE: This procedure is rather... interesting and derived from legacy code I wrote in Autohotkey years
        # ago. It features some rather interesting Windows quirks.

        if not icon_file.endswith(".ico"):
            icon_file += ".ico"

        desktop_ini_file = os.path.join(directory, "desktop.ini")
        relative_path = os.path.relpath(icon_file, directory)

        # If the file already exists, set the attributes in a way that the program can edit the file:
        # -r : Clears read-only state
        # -s : Clears the system file attribute
        # -h : Clears the hidden state
        if os.path.isfile(desktop_ini_file):
            Popen(["attrib", "-s", "-h", "-r", desktop_ini_file]).wait()

        # Write the folder icon information to the desktop.ini file, deleting all previous content of the file
        with open(desktop_ini_file, 'w') as f:
            f.writelines(["[.ShellClassInfo]",          # This is a shebang-like construct for Windows to know what to do
                          "IconFile=" + relative_path,  # This sets the path to the icon file
                          "IconIndex=0",                # The rest is just some metadata stuff
                          "[ViewState]",
                          "Mode=",
                          "Vid=",
                          "FolderType=Videos"])

        # Set the attributes of the desktop.ini file to hidden, system file and read-only
        Popen(["attrib", "+s", "+h", "+r", desktop_ini_file]).wait()
        # Set the directory to read-only? What on earth? Windows is weird.
        Popen(["attrib", "+r", directory]).wait()

    @staticmethod
    def reset_iconization_state(directory: str) -> None:
        """
        Resets the iconization state of the given directory by simply deleting the desktop.ini file
        :param directory: the directory to de-iconize
        :return:          None
        """
        if os.path.isfile(os.path.join(directory, "desktop.ini")):
            os.remove(os.path.join(directory, "desktop.ini"))

    @staticmethod
    def get_icon_file(directory: str) -> str:
        """
        Returns the path to the given directory's icon file, if it is iconized. If not, None is returned

        :param directory: The directory to check
        :return:          Either the path to the icon file or None if no icon file exists
        """
        with open(os.path.join(directory, "desktop.ini"), 'r') as desktop_ini_file:
            desktop_ini = desktop_ini_file.read()

        if "IconFile=" in desktop_ini:
            return desktop_ini.split("IconFile=")[1].split("\n")[0]

    @staticmethod
    def get_procedure_name() -> str:
        """
        :return: The name of the Procedure
        """
        return "desktop_ini"
