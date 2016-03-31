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

# imports
try:
    from cli.GenericCli import GenericCli
    from Globals import Globals
except ImportError:
    from media_manager.cli.GenericCli import GenericCli
    from media_manager.Globals import Globals


class MainCli(GenericCli):
    """
    Class that implements the Main CLI
    """

    def __init__(self, active_plugins) -> None:
        """
        Constructor
        :param active_plugins: The plugins to be displayed
        :return: void
        """
        super().__init__()
        self.plugins = active_plugins

    def start(self) -> None:
        """
        Adds buttons for all plugins
        :return: void
        """
        print("MEDIA MANAGER VERSION " + Globals.version_no + "\n\n")
        print("Available Plugins:\n\n")

        plugin_dict = {}
        plugin_list = []

        i = 1
        for plugin in self.plugins:
            plugin_list.append("\t" + str(i) + ". " + plugin.get_name() + "\n")
            plugin_dict[i] = plugin
            i += 1

        for entry in plugin_list:
            print(entry)

        while True:
            user_input = input("Select plugin by entering the plugin index number.\n"
                               "To exit, enter 'exit' or 'quit'\n"
                               "To get the list of plugins again, enter 'list'\n")
            try:
                plugin_dict[int(user_input)].start_cli(self)
            except (KeyError, ValueError):
                if user_input.lower() in ["quit", "exit"]:
                    self.stop()
                elif user_input.lower() == "list":
                    for entry in plugin_list:
                        print(entry)
                else:
                    print("Unrecognized Command\n")
