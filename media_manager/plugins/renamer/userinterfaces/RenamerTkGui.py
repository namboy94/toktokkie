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
    from media_manager.plugins.renamer.utils.Renamer import Renamer
    from media_manager.guitemplates.tk.GenericTkGui import GenericTkGui
except ImportError:
    from plugins.renamer.utils.Renamer import Renamer
    from guitemplates.tk.GenericTkGui import GenericTkGui

from tkinter import END


class RenamerTkGui(GenericTkGui):
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
        self.browser = None
        super().__init__("Renamer", parent, True)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return void
        """
        self.button = self.generate_simple_button("Start", self.start_rename)
        self.button.grid(column=4, row=0)

        self.browser = self.generate_simple_button("Browse", self.browse_directory)
        self.browser.grid(column=0, row=0)

        self.entry = self.generate_text_entry("", self.start_rename)
        self.entry.grid(columnspan=2, column=1, row=0)

    def start_rename(self, *kwargs):
        """
        Starts the renaming process
        :param kwargs: used as a dummy element to run the method despite receiving too many arguments
        :return: void
        """

        if len(kwargs) == -1:
            return

        try:
            abs_dir = self.entry.get()
            renamer = Renamer(abs_dir)
            confirmation = renamer.request_confirmation()
            if self.confirmer(confirmation):
                renamer.confirm(confirmation)
                renamer.start_rename()
        except Exception as e:
            if str(e) == "Not a directory":
                self.show_message_dialog("Not a directory", "Please enter a valid directory path")
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

    def browse_directory(self, widget):
        """
        Opens a directory browser dialog.
        :param widget: the button that started this mess
        :return: void
        """
        if widget is None:
            return

        directory = self.show_directory_chooser_dialog()
        if directory:
            self.entry.delete(0, END)
            self.entry.insert(0, directory)
