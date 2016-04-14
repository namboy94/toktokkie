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

# imports
from argparse import Namespace
from typing import Tuple, List, Dict
from gfworks.interfaces.GenericWindow import GenericWindow

try:
    from cli.GenericCli import GenericCli
    from plugins.common.GenericPlugin import GenericPlugin
    from plugins.iconizer.userinterfaces.IconizerGui import IconizerGui
    from plugins.iconizer.userinterfaces.IconizerCli import IconizerCli
except ImportError:
    from media_manager.cli.GenericCli import GenericCli
    from media_manager.plugins.common.GenericPlugin import GenericPlugin
    from media_manager.plugins.iconizer.userinterfaces.IconizerGui import IconizerGui
    from media_manager.plugins.iconizer.userinterfaces.IconizerCli import IconizerCli


class IconizerPlugin(GenericPlugin):
    """
    Class that handles the calls to the Iconizer Plugin.

    It offers methods to start the plugin in CLI-args, CLI-interactive and GUI mode
    """

    def get_name(self) -> str:
        """
        This method returns the name of the Plugin for display purposes

        :return: the name of this plugin
        """
        return "Iconizer"

    def get_config_tag(self) -> str:
        """
        This method returns the tag used to enable or disable this plugin
        in the config file of media-manager.

        :return: the config tag of this plugin
        """
        return "iconizer"

    def get_command_name(self) -> str:
        """
        This method return the command name used by the argument parser
        when using the argument-driven CLI

        :return: the command that starts this plugin
        """
        return "iconizer"

    def get_parser_arguments(self) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """
        This returns all command line arguments to be added to the Argument Parser for this
        plugin. There are two types of arguments: The ones that ask for strings and the others
        that ask for boolean values.

        To separate these, a tuple structure is used. The tuple's first element contains the
        arguments that ask for boolean values, whereas the second element asks for string values

        The tuple elements are lists of dictionaries. The dictionaries contain the actual
        arguments to be used.

        Every dictionary in the list has a 'tag' key that points to the argument used in the
        --argument fashion from the command line as well as a 'desc' key that points to a
        short description of the parameter.

        :return: the tuple of lists of dictionaries described above
        """
        return ([{"tag": "iconizer-use-nautilus", "desc": "Use the nautilus iconizer"},
                 {"tag": "iconizer-use-nemo", "desc": "Use the nemo iconizer"}],

                [{"tag": "iconizer-directory", "desc": "The Directory to be iconized by the iconizer"}])

    def start_args_parse(self, args: Namespace) -> None:
        """
        Runs the plugin in arg parse mode
        The arguments must have been parsed beforehand by the MainArgsParser class

        :param args: The parsed argument Namespace
        :return: None
        """
        # Check if the combination of arguments is valid
        valid = False
        if getattr(args, "iconizer-directory"):
            if getattr(args, "iconizer_use_nautilus") ^ \
                    getattr(args, "iconizer_use_nemo"):
                valid = True

        if valid:
            # If they're valid, run the CLI in argument mode

            directory = getattr(args, "iconizer-directory")

            if getattr(args, "iconizer_use_nautilus"):
                # noinspection PyTypeChecker
                IconizerCli(None).mainloop(directory, "Nautilus")
            elif getattr(args, "iconizer_use_nemo"):
                # noinspection PyTypeChecker
                IconizerCli(None).mainloop(directory, "Nemo")
        else:
            # Otherwise let the user know that the combination was wrong
            print("Invalid argument combination passed")

    def start_cli(self, parent_cli: GenericCli) -> None:
        """
        Starts the CLI of the plugin in interactive mode

        :param parent_cli: the parent cli to which the plugin can return to
        :return: None
        """
        IconizerCli(parent_cli).start()

    def start_gui(self, parent_gui: GenericWindow) -> None:
        """
        Starts the GUI of the plugin

        :param parent_gui: the gui's parent to which the plugin can return to
        :return: None
        """
        IconizerGui(parent_gui).start()
