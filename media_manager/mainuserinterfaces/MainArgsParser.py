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

import argparse
import sys


class MainArgsParser(object):
    """
    Class that implements an Argument Parser that enables non-interactive use of the media manager program
    """

    def __init__(self, active_plugins) -> None:
        """
        Constructor
        :param active_plugins: The plugins to be enabled
        :return: void
        """
        self.plugins = active_plugins

    def run(self):
        parser = argparse.ArgumentParser()

        for plugin in self.plugins:
            parser.add_argument("--" + plugin.get_command_name(),
                                help="Starts plugin " + plugin.get_name(), action="store_true")
            for argument in plugin.get_parser_arguments()[0]:
                parser.add_argument("--" + argument["tag"], help=argument["desc"], action="store_true")
            for argument in plugin.get_parser_arguments()[1]:
                parser.add_argument("--" + argument["tag"], help=argument["desc"], dest=argument["tag"])
        args = parser.parse_args()

        exactly_one_plugin = False

        for plugin in self.plugins:
            if getattr(args, plugin.get_command_name().replace("-", "_")):
                if not exactly_one_plugin:
                    exactly_one_plugin = True
                elif exactly_one_plugin:
                    print("Illegal argument combination. Only select one plugin at a time")
                    sys.exit(1)

        for plugin in self.plugins:
            if getattr(args, plugin.get_command_name().replace("-", "_")):
                if len(sys.argv) == 2:
                    plugin.start_cli(None)
                else:
                    plugin.start_args_parse(args)
