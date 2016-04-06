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

try:
    from plugins.common.GenericPlugin import GenericPlugin
    from plugins.showmanager.userinterfaces.ShowManagerGUI import ShowManagerGui
    from plugins.showmanager.userinterfaces.ShowManagerCli import ShowManagerCli
    from Globals import Globals
except ImportError:
    from media_manager.plugins.common.GenericPlugin import GenericPlugin
    from media_manager.plugins.showmanager.userinterfaces.ShowManagerGui import ShowManagerGui
    from media_manager.plugins.showmanager.userinterfaces.ShowManagerCli import ShowManagerCli
    from media_manager.Globals import Globals


class ShowManagerPlugin(GenericPlugin):
    """
    Class that handles the calls to the Show Manager
    """

    def get_name(self) -> str:
        """
        :return: "Batch Download Manager"
        """
        return "Show Manager"

    def get_config_tag(self) -> str:
        """
        :return: "batch-download"
        """
        return "show-manager"

    def get_command_name(self) -> str:
        """
        :return: "batch download"
        """
        return "show-manager"

    def get_parser_arguments(self):
        """
        :return: tuple of two list of dictionaries, consisting of argument tags and descriptions.
                    the first tuple element contains boolean values, the others store string values
        """
        return ([],
                [])

    def start_args_parse(self, args):
        """
        Runs the plugin in arg parse mode
        """
        valid = False

        if valid:
            print("Do Stuff")
        else:
            print("Invalid argument combination passed")

    def start_cli(self, parent_cli):
        """
        Starts the CLI of the plugin
        :param parent_cli: the parent cli
        :return: void
        """
        ShowManagerCli(parent_cli).start()

    def start_gui(self, parent_gui: Globals.selected_grid_gui_framework):
        """
        Starts the GUI, while hiding the parent until finished
        :param parent_gui: the parent gui window
        :return: void
        """
        ShowManagerGui(parent_gui).start()
