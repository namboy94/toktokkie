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

try:
    from plugins.common.GenericPlugin import GenericPlugin
    from plugins.iconizer.userinterfaces.IconizerGui import IconizerGui
    from plugins.iconizer.userinterfaces.IconizerCli import IconizerCli
except ImportError:
    from media_manager.plugins.common.GenericPlugin import GenericPlugin
    from media_manager.plugins.iconizer.userinterfaces.IconizerGui import IconizerGui
    from media_manager.plugins.iconizer.userinterfaces.IconizerCli import IconizerCli


class IconizerPlugin(GenericPlugin):
    """
    Class that handles iconizing of folders
    """

    def get_name(self):
        """
        :return "Iconizer"
        """
        return "Iconizer"

    def get_config_tag(self):
        """
        :return "iconizer"
        """
        return "iconizer"

    def get_command_name(self):
        """
        :return "iconizer"
        """
        return "iconizer"

    def get_parser_arguments(self):
        """
        :return: tuple of two list of dictionaries, consisting of argument tags and descriptions.
                    the first tuple element contains boolean values, the others store string values
        """
        return ([{"tag": "iconizer-use-nautilus", "desc": "Use the nautilus iconizer"},
                 {"tag": "iconizer-use-nemo", "desc": "Use the nemo iconizer"}],

                [{"tag": "iconizer-directory", "desc": "The Directory to be iconized by the iconizer"}])

    def start_args_parse(self, args):
        """
        Runs the plugin in arg parse mode
        """
        valid = False
        if getattr(args, "iconizer-directory"):
            if getattr(args, "iconizer_use_nautilus") ^ \
                    getattr(args, "iconizer_use_nemo"):
                valid = True

        if valid:
            cli = None
            if getattr(args, "iconizer_use_nautilus"):
                cli = IconizerCli(None, "Nautilus")
            elif getattr(args, "iconizer_use_nemo"):
                cli = IconizerCli(None, "Nemo")
            cli.mainloop(getattr(args, "iconizer-directory"))
        else:
            print("Invalid argument combination passed")

    def start_cli(self, parent_cli):
        """
        Starts the CLI of the plugin
        :param parent_cli: the parent cli
        :return: void
        """
        IconizerCli(parent_cli).start()

    def start_gui(self, parent_gui):
        """
        Starts the GUI, while hiding the parent until finished
        :param parent_gui: the parent window
        :return void
        """
        IconizerGui(parent_gui).start()
