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
    from plugins.renamer.userinterfaces.RenamerGUI import RenamerGUI
    from plugins.renamer.userinterfaces.RenamerCli import RenamerCli
except ImportError:
    from media_manager.plugins.common.GenericPlugin import GenericPlugin
    from media_manager.plugins.renamer.userinterfaces.RenamerGUI import RenamerGUI
    from media_manager.plugins.renamer.userinterfaces.RenamerCli import RenamerCli


class RenamerPlugin(GenericPlugin):
    """
    Class that handles renaming of episodes
    """

    def get_name(self):
        """
        :return "Renamer"
        """
        return "Renamer"

    def get_config_tag(self):
        """
        :return "renamer"
        """
        return "renamer"

    def get_command_name(self):
        """
        :return "renamer"
        """
        return "renamer"

    def start_cli(self, parent_cli):
        """
        Starts the CLI of the plugin
        :param parent_cli: the parent cli
        :return: void
        """
        RenamerCli(parent_cli).start()

    def start_gui(self, parent_gui):
        """
        Starts the GUI, while hiding the parent until finished
        :param parent_gui: the parent gui window
        :return void
        """
        RenamerGUI(parent_gui).start()
