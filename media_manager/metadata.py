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

# This checks for each user interface if they are installed
try:
    from gfworks.templates.gtk3.Gtk3GridTemplate import Gtk3GridTemplate
except ImportError:
    Gtk3GridTemplate = None

try:
    from gfworks.templates.tk.TkGridTemplate import TkGridTemplate
except ImportError:
    TkGridTemplate = None


class Globals(object):
    """
    A class that stores the currently selected GUI framework to enable cross-platform use using
    gfworks. Future plans of gfworks may be able to make this admittedly ugly construct
    obsolete, but as of right now it is required
    """

    selected_grid_gui_framework = TkGridTemplate
    """
    This stores the selected GUI framework, it is initialized as TkGridTemplate to avoid NoneType
    errors. The variable will be correctly set at some point in the main module's main method as
    either Gtk3GridTemplate or TkGridTemplate.
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

project_name = "media-manager"
"""
The name of the project
"""

project_description = "A personal media manager program"
"""
A short description of the project
"""

version_number = "0.9.5.1"
"""
The current version of the program.
"""

project_url = "http://namibsun.net/namboy94/media-manager"
"""
A URL linking to the home page of the project, in this case a
self-hosted Gitlab page
"""

download_url = "http://gitlab.namibsun.net/namboy94/media-manager/repository/archive.zip?ref=master"
"""
A URL linking to the current source zip file.
"""

author_name = "Hermann Krumrey"
"""
The name(s) of the project author(s)
"""

author_email = "hermann@krumreyh.com"
"""
The email address(es) of the project author(s)
"""

license_type = "GNU GPL3"
"""
The project's license type
"""