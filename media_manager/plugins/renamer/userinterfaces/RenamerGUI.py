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
    from metadata import Globals
except ImportError:
    from media_manager.plugins.renamer.utils.Renamer import Renamer
    from media_manager.metadata import Globals


class RenamerGUI(Globals.selected_grid_gui_framework):
    """
    GUI for the Renamer plugin
    """

    def __init__(self, parent):
        """
        Constructor
        :param parent: the parent gui window
        :return: void
        """
        self.button = None
        self.entry = None
        self.browse = None
        super().__init__("Renamer", parent, True)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return: void
        """
        self.button = self.generate_button("Start", self.start_rename)
        self.position_absolute(self.button, 4, 0, 1, 1)

        self.browse = self.generate_button("Browse", self.browse_directory)
        self.position_absolute(self.browse, 0, 0, 1, 1)

        self.entry = self.generate_text_entry("", self.start_rename)
        self.position_absolute(self.entry, 1, 0, 2, 1)

    def start_rename(self, widget):
        """
        Starts the renaming process
        :param widget: the button that started this method
        :return: void
        """
        if widget is None:
            return
        try:
            abs_dir = self.get_string_from_text_entry(self.entry)
            renamer = Renamer(abs_dir)
            confirmation = renamer.request_confirmation()
            if self.confirmer(confirmation):
                renamer.confirm(confirmation)
                renamer.start_rename()
        except Exception as e:
            if str(e) == "Not a directory":
                self.show_message_dialog("Error, ", str(e))
            else:
                raise e

    def browse_directory(self, widget):
        """
        Shows a directory chooser dialog and sets the entry to the result of the browse
        :param widget: the button that called this method
        :return: void
        """
        if widget is not None:
            selected_directory = self.show_directory_chooser_dialog()
            if selected_directory:
                self.set_text_entry_string(self.entry, selected_directory)

    def confirmer(self, confirmation):
        """
        Asks the user for confirmation before continuing the rename
        :param confirmation: the confirmation
        :return: False if the user did not confirm the rename, True otherwise.
        """
        i = 0
        while i < len(confirmation[0]):
            message = "Rename\n"
            message += confirmation[0][i]
            message += "\nto\n"
            message += confirmation[1][i]
            message += "\n?"
            response = self.show_yes_no_dialog("Confirmation", message)
            if not response:
                return False
            i += 1
        return True
