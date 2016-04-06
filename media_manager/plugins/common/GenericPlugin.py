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


class GenericPlugin(object):
    """
    Generic Plugin that serves as a unified interface for the plugins.
    """

    def get_name(self):
        """
        :return: the name of this plugin
        """
        raise NotImplementedError()

    def get_command_name(self):
        """
        :return: the command that starts ths plugin
        """
        raise NotImplementedError()

    def get_config_tag(self):
        """
        :return: the config tag of this plugin
        """
        raise NotImplementedError()

    def get_parser_arguments(self):
        """
        :return: tuple of two list of dictionaries, consisting of argument tags and descriptions.
                    the first tuple element contains boolean values, the others store string values
        """
        raise NotImplementedError()

    def start_args_parse(self, args):
        """
        Runs the plugin in arg parse mode
        """
        raise NotImplementedError()

    def start_cli(self, parent_cli):
        """
        Starts the CLI of the plugin
        :param parent_cli: the parent cli
        :return: void
        """
        raise NotImplementedError()

    def start_gui(self, parent_gui):
        """
        Starts the GUI of the plugin
        :param parent_gui: the gui's parent
        :return: void
        """
        raise NotImplementedError()
