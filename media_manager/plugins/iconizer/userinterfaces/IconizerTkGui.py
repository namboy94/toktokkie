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

import os
from tkinter import END

try:
    from media_manager.guitemplates.tk.GenericTkGui import GenericTkGui
    from media_manager.plugins.iconizer.utils.DeepIconizer import DeepIconizer
except ImportError:
    from guitemplates.tk.GenericTkGui import GenericTkGui
    from plugins.iconizer.utils.DeepIconizer import DeepIconizer


class IconizerTkGui(GenericTkGui):
    """
    GUI for the Iconizer plugin
    """

    def __init__(self, parent):
        """
        Constructor
        :return: void
        """
        self.directory_entry = None
        self.directory_browse_button = None
        self.start_button = None
        self.iconizer_method_combo_box = None
        super().__init__("Iconizer", parent, True)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return: void
        """
        self.directory_entry = self.generate_text_entry("Enter Directory here", self.iconize_start)
        self.directory_entry.grid(columnspan=3, column=0, row=0)

        self.directory_browse_button = self.generate_simple_button("Browse", self.browse_directory)
        self.directory_browse_button.grid(column=1, row=1)

        self.start_button = self.generate_simple_button("Start", self.iconize_start)
        self.start_button.grid(column=3, row=1)

        self.iconizer_method_combo_box = self.generate_combo_box(DeepIconizer.get_iconizer_options())
        self.iconizer_method_combo_box.grid(column=3, row=0)

    def iconize_start(self, widget):
        """
        Starts the iconizing process
        :param widget: the widget that started this method
        :return void
        """
        if widget is None:
            return

        directory = self.directory_entry.get()
        if not os.path.isdir(directory):
            self.show_message_dialog("Not a directory!", "Please enter a valid directory path.")
            return
        children = os.listdir(directory)
        multiple = True
        for child in children:
            if child == ".icons":
                multiple = False
                break

        if multiple:
            for child in children:
                self.iconize_dir(os.path.join(directory, child))
        else:
            self.iconize_dir(directory)

    def iconize_dir(self, directory):
        """
        Iconizes a single folder
        :param directory: the directory to be iconized
        :return: void
        """
        method = self.iconizer_method_combo_box.get()
        has_icons = False
        for sub_directory in os.listdir(directory):
            if sub_directory == ".icons":
                has_icons = True
                break
        if not has_icons:
            print("Error, " + directory + " has no subdirectory \".icons\"")

        DeepIconizer(directory, method).iconize()

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
            self.directory_entry.delete(0, END)
            self.directory_entry.insert(0, directory)
