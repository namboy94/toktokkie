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

from gfworks.templates.gtk3.Gtk3GridTemplate import Gtk3GridTemplate
from gfworks.templates.tk.TkGridTemplate import TkGridTemplate


class Globals(object):
    """
    A class that stores the currently selected GUI framework to enable cross-platform use using
    gfworks. Future plans of gfworks may be able to make this admittedly ugly construct
    obsolete, but as of right now it is required
    """

    selected_grid_gui_framework = None
    """
    This stores the selected GUI framework, it is initialized as None and will be initialized
    at some point in the main module's main method as either Gtk3GridTemplate or TkGridTemplate
    """

    gtk3_gui_template = Gtk3GridTemplate
    """
    A constant variable that stores the GTK 3 Grid Template class type
    """

    tk_gui_template = TkGridTemplate
    """
    A constant variable that stores the Tk Grid Template class type
    """


"""
The metadata is stored here. It can be used by any other module in this project this way, most
notably by the setup.py file
"""

version_number = "0.9.1.2"
"""
The current version of the program.
"""
