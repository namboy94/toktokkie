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


from plugins.renamer.utils.Renamer import Renamer
from guitemplates.gtk.GenericGtkGui import GenericGtkGui


class RenamerGUI(GenericGtkGui):
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
        super().__init__("Renamer", parent, True)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return void
        """
        self.button = self.generate_simple_button("Start", self.start_rename)
        self.grid.attach(self.button, 4, 0, 1, 1)

        self.entry = self.generate_text_entry("", self.start_rename)
        self.grid.attach(self.entry, 0, 0, 3, 1)

    def start_rename(self, widget):
        """
        Starts the renaming process
        :param widget: the button that started this method
        :return: void
        """
        if widget is None:
            return
        try:
            abs_dir = self.entry.get_text()
            renamer = Renamer(abs_dir)
            confirmation = renamer.request_confirmation()
            if self.confirmer(confirmation):
                renamer.confirm(confirmation)
                renamer.start_rename()
        except Exception as e:
            if str(e) == "Not a directory":
                self.show_message_dialog(str(e))
            else:
                raise e

    def confirmer(self, confirmation):
        """
        Asks the user for confirmation before continuing the rename
        :param confirmation: the confirmation
        :return False if the user did not confirm the rename, True otherwise.
        """
        i = 0
        while i < len(confirmation[0]):
            message = "Rename\n"
            message += confirmation[0][i]
            message += "\nto\n"
            message += confirmation[1][i]
            message += "\n?"
            response = self.show_y_n_dialog("Confirmation", message)
            if not response:
                return False
            i += 1
        return True
