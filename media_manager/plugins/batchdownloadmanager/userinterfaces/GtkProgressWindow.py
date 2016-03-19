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

from gi.repository import GObject

GObject.threads_init()

try:
    from media_manager.guitemplates.gtk.GenericGtkGui import GenericGtkGui
except ImportError:
    from guitemplates.gtk.GenericGtkGui import GenericGtkGui


class GtkProgressWindow(GenericGtkGui):
    """
    Download Progress Window in GTK
    """

    def __init__(self, parent):
        """
        Constructor
        :param parent: the parent gui
        :return: void
        """
        # Initialization
        self.title = None
        super().__init__("Batch Download Manager", parent, False)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return: void
        """
        self.title = self.generate_label("Title")
        self.grid.attach(self.title, 0, 0, 1, 1)

    def update(self):
        self.title.set_text("updated")
