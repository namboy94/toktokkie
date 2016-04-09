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
    from plugins.renamer.utils.Renamer import Renamer
    from cli.exceptions.ReturnException import ReturnException
    from cli.GenericCli import GenericCli
except ImportError:
    from media_manager.plugins.renamer.utils.Renamer import Renamer
    from media_manager.cli.exceptions.ReturnException import ReturnException
    from media_manager.cli.GenericCli import GenericCli


class RenamerCli(GenericCli):
    """
    CLI for the Renamer plugin
    """

    def __init__(self, parent):
        """
        Constructor
        :param parent: the parent cli
        :return: void
        """
        super().__init__(parent)

    def start(self, title=None):
        """
        Starts the plugin main loop
        :return: void
        """
        super().start("RENAMER PLUGIN\n")

    def mainloop(self, directory=None):
        """
        Starts the renaming process
        :return: void
        """
        if directory is None:
            directory = self.ask_user("Enter the show/series directory path:\n")

        try:
            renamer = Renamer(directory)
            confirmation = renamer.request_confirmation()
            if self.confirmer(confirmation):
                print("Renaming...")
                renamer.confirm(confirmation)
                renamer.start_rename()
                print("Renaming successful.")
            else:
                print("Renaming cancelled.")
        except Exception as e:
            if str(e) == "Not a directory":
                print("Entered directory is not valid\n")

    @staticmethod
    def confirmer(confirmation):
        """
        Asks the user for confirmation before continuing the rename
        :param confirmation: the confirmation
        :return: False if the user did not confirm the rename, True otherwise.
        """
        i = 0
        while i < len(confirmation[0]):
            print("OLD: " + confirmation[0][i])
            print("NEW: " + confirmation[1][i] + "\n")
            i += 1
        response = input("Proceed with renaming? This can not be undone. (y/n)")

        return response == "y"
