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
import argparse
import sys
from typing import List

try:
    from modules.hooks.GenericPlugin import GenericPlugin
except ImportError:
    from modules.hooks.GenericPlugin import GenericPlugin


class MainArgsParser(object):
    """
    Class that implements an Argument Parser that enables non-interactive use
    of the media manager program

    It defines a Argument Parser that queries the different possible options
    from the currently active modules
    """

    active_plugins = []
    """
    A list of the active modules, established via the constructor
    """

    # noinspection PyTypeChecker
    def __init__(self, active_plugins: List[GenericPlugin]) -> None:
        """
        Constructor of the MainArgsParser

        It stores the active modules as a local lost variable

        :param active_plugins: The modules to be enabled
        :return: None
        """
        self.plugins = active_plugins

    def run(self) -> None:
        """
        Runs the argument parser.

        It sets up the argument parser first, getting the arguments from the active
        modules, then parses them and acts according to the user's input in
        conclusion.

        :return: None
        """
        # Creates a new ArgumentParser object
        parser = argparse.ArgumentParser()

        # Gets command line options from all active modules
        for plugin in self.plugins:
            # This adds the option to specify which plugin will be used
            parser.add_argument("--" + plugin.get_command_name(),
                                help="Starts plugin " + plugin.get_name(), action="store_true")
            # This adds additional True/False flag values to the argument parser
            for argument in plugin.get_parser_arguments()[0]:
                parser.add_argument("--" + argument["tag"], help=argument["desc"], action="store_true")
            # This adds additional String storing options to the argument parser
            for argument in plugin.get_parser_arguments()[1]:
                parser.add_argument("--" + argument["tag"], help=argument["desc"], dest=argument["tag"])

        # This parses the arguments
        args = parser.parse_args()

        # This is a check that there is only one plugin selected.
        # If this is not the case, the passed arguments are rejected as an invalid
        # argument combination and the program ends
        exactly_one_plugin = False
        for plugin in self.plugins:
            # getattr is used in conjunction with replace("-", "_") because the
            # argument parser mangles the names somehow
            if getattr(args, plugin.get_command_name().replace("-", "_")):
                if not exactly_one_plugin:  # If this is the first found plugin
                    exactly_one_plugin = True
                elif exactly_one_plugin:  # If another plugin was already found
                    print("Illegal argument combination. Only select one plugin at a time")
                    sys.exit(1)

        # This now runs the plugin.
        plugin_run = False
        for plugin in self.plugins:
            # getattr is used in conjunction with replace("-", "_") because the
            # argument parser mangles the names somehow
            if getattr(args, plugin.get_command_name().replace("-", "_")):
                if len(sys.argv) == 2:
                    # This just starts the CLI of that plugin in interactive mode
                    # noinspection PyTypeChecker
                    plugin.start_cli(None)
                else:
                    # This runs the plugin in true argument-passing mode
                    plugin.start_args_parse(args)
                plugin_run = True

        if not plugin_run:
            print("No valid plugin specified")
