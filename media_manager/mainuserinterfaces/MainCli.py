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
try:
    from cli.GenericCli import GenericCli
    from cli.exceptions.ReturnException import ReturnException
    from Globals import Globals
except ImportError:
    from media_manager.cli.GenericCli import GenericCli
    from media_manager.cli.exceptions.ReturnException import ReturnException
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

    def start(self, title=None) -> None:
        """
        Starts the CLI
        :return: void
        """
        super().start("MEDIA MANAGER VERSION " + Globals.version_no + "\n\n" + "Available Plugins:")

    def mainloop(self):
        """
        The main loop of the CLI
        :return: void
        """
        print()

        plugin_dict = {}
        plugin_list = []

        i = 1
        for plugin in self.plugins:
            plugin_list.append("\t" + str(i) + ". " + plugin.get_name())
            plugin_dict[i] = plugin
            i += 1

        for entry in plugin_list:
            print(entry)

        while True:
            user_input = self.ask_user("\nSelect plugin by entering the plugin index number."
                                       "\nTo exit, enter 'exit' or 'quit'"
                                       "\nTo get the list of plugins again, enter 'list'\n")
            try:
                print()
                plugin_dict[int(user_input)].start_cli(self)
                return
            except (KeyError, ValueError):
                if user_input.lower() == "list":
                    for entry in plugin_list:
                        print(entry)
                else:
                    print("Unrecognized Command")
