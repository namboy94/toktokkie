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
from typing import Dict, Tuple, List
from gfworks.interfaces.GenericWindow import GenericWindow

try:
    from cli.GenericCli import GenericCli
except ImportError:
    from tok_tokkie.cli.GenericCli import GenericCli


class GenericPlugin(object):
    """
    Generic Plugin that serves as a unified interface for the media manager plugins.

    It defines multiple methods that give information about the plugin, as well
    as methods to start the GUI, interactive CLI or argument-driven CLI
    """

    def get_name(self) -> str:
        """
        This method returns the name of the Plugin for display purposes

        :return: the name of this plugin
        """
        raise NotImplementedError()

    def get_command_name(self) -> str:
        """
        This method return the command name used by the argument parser
        when using the argument-driven CLI

        :return: the command that starts this plugin
        """
        raise NotImplementedError()

    def get_config_tag(self) -> str:
        """
        This method returns the tag used to enable or disable this plugin
        in the config file of media-manager.

        :return: the config tag of this plugin
        """
        raise NotImplementedError()

    def get_parser_arguments(self) -> Tuple[List[Dict[str, str]]]:
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
        raise NotImplementedError()

    def start_args_parse(self, args: Namespace) -> None:
        """
        Runs the plugin in arg parse mode
        The arguments must have been parsed beforehand by the MainArgsParser class

        :param args: The parsed argument Namespace
        :return: None
        """
        raise NotImplementedError()

    def start_cli(self, parent_cli: GenericCli) -> None:
        """
        Starts the CLI of the plugin in interactive mode

        :param parent_cli: the parent cli to which the plugin can return to
        :return: None
        """
        raise NotImplementedError()

    def start_gui(self, parent_gui: GenericWindow) -> None:
        """
        Starts the GUI of the plugin

        :param parent_gui: the gui's parent to which the plugin can return to
        :return: None
        """
        raise NotImplementedError()
