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

try:
    from cli.GenericCli import GenericCli
    from cli.exceptions.ReturnException import ReturnException
    from plugins.iconizer.utils.DeepIconizer import DeepIconizer
except ImportError:
    from media_manager.cli.GenericCli import GenericCli
    from media_manager.cli.exceptions.ReturnException import ReturnException
    from media_manager.plugins.iconizer.utils.DeepIconizer import DeepIconizer


class IconizerCli(GenericCli):
    """
    GCLI for the Iconizer plugin
    """

    def __init__(self, parent, selected_iconizer=None):
        """
        Constructor
        :return: void
        """
        self.selected_iconizer = selected_iconizer
        super().__init__(parent)

    def start(self, title=None):
        """
        Starts the plugin main loop
        :return void
        """
        super().start("ICONIZER PLUGIN\n")

    def mainloop(self, directory=None):
        """
        Starts the iconizing process
        :return void
        """

        if directory is None:
            directory = self.ask_user("Enter the directory to iconize:\n")

        if not os.path.isdir(directory):
            print("No valid directory entered")
            return

        if directory is None:

            print("Which iconizing method would you like to use?\n")
            i = 1
            iconizer_dict = {}
            for option in DeepIconizer.get_iconizer_options():
                print(str(i) + ":" + option)
                iconizer_dict[i] = option
                i += 1

            iconizer_selected = False
            while not iconizer_selected:
                user_iconizer = self.ask_user()
                try:
                    self.selected_iconizer = iconizer_dict[int(user_iconizer)]
                    iconizer_selected = True
                except (ValueError, KeyError):
                    print("Invalid selection. Please enter the index of the preferred iconizer method\n")

        children = os.listdir(directory)
        multiple = True
        for child in children:
            if child == ".icons":
                multiple = False
                break

        print("Iconizing Start")

        if multiple:
            for child in children:
                self.iconize_dir(os.path.join(directory, child))
        else:
            self.iconize_dir(directory)
        print("Iconizing End")

    def iconize_dir(self, directory):
        """
        Iconizes a single folder
        :param directory: the directory to be iconized
        :return: void
        """
        if not os.path.isdir(directory):
            return

        print("Iconizing " + directory)
        method = self.selected_iconizer
        has_icons = False
        for sub_directory in os.listdir(directory):
            if sub_directory == ".icons":
                has_icons = True
                break
        if not has_icons:
            print("Error, " + directory + " has no subdirectory \".icons\"")
            return

        DeepIconizer(directory, method).iconize()
