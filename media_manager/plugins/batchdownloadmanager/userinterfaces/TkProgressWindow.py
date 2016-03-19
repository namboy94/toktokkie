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

from tkinter import END, W, E, N, S, Grid

try:
    from media_manager.guitemplates.tk.GenericTkGui import GenericTkGui
except ImportError:
    from guitemplates.tk.GenericTkGui import GenericTkGui


class TkProgressWindow(GenericTkGui):
    """
    Download Progress Window in TK
    """

    def __init__(self, parent):
        """
        Constructor
        :param parent: the parent gui
        :return: void
        """
        # Initialize GUI
        self.title = None
        super().__init__("Batch Download Manager", parent, False)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return: void
        """
        self.title = self.generate_label("Title")
        self.title.grid(columnspan=2, column=2, row=1, sticky=W + E + N + S)

    def update(self):
        self.title.delete(0, END)
        self.title.insert("updated")
