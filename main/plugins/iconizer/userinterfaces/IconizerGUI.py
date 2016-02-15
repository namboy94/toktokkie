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
from gi.repository import Gtk
from plugins.genericPlugin.userinterfaces.GenericGUI import GenericGUI
from plugins.iconizer.utils.DeepIconizer import DeepIconizer

"""
GUI for the Iconizer plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class IconizerGUI(GenericGUI):

    """
    Sets up all interface elements of the GUI
    """
    def setUp(self):

        self.directoryEntry = self.generateEntry("Enter Directory here", self.iconizeStart)
        self.grid.attach(self.directoryEntry, 0, 0, 3, 2)

        self.startButton = self.generateSimpleButton("Start", self.iconizeStart)
        self.grid.attach_next_to(self.startButton, self.directoryEntry, Gtk.PositionType.RIGHT, 1, 1)

        self.iconizerMethodComboBox = self.generateComboBox(["Nautilus", "Nemo"])
        self.grid.attach_next_to(self.iconizerMethodComboBox[0], self.startButton, Gtk.PositionType.BOTTOM, 1, 1)

    """
    Starts the iconizing process
    """
    def iconizeStart(self, widget):
        directory = self.directoryEntry.get_text()
        if not directory.endswith("/"):
            directory += "/"
        if not os.path.isdir(directory):
            self.messageBox("Not a directory!")
            return
        children = os.listdir(directory)
        multiple = True
        for child in children:
            if child == ".icons":
                multiple = False
                break

        if multiple:
            for child in children:
                self.iconizeDir(directory + child)
        else: self.iconizeDir(directory)

    """
    Iconizes a single folder
    @:param - directory - the directory to be iconized
    """
    def iconizeDir(self, directory):
        method = self.getCurrentSelectedComboBox(self.iconizerMethodComboBox)
        hasIcons = False
        for subDirectory in os.listdir(directory):
            if subDirectory == ".icons":
                hasIcons = True
                break
        if not hasIcons:
            print("Error, " + directory + " has no subdirectory \".icons\"")

        DeepIconizer(directory, method).iconize()