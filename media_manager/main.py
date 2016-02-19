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

import configparser
import os

try:
    from media_manager.mainuserinterfaces.MainGUI import MainGUI
    from media_manager.mainuserinterfaces.MainTkGui import MainTkGui
    from media_manager.plugins.PluginManager import PluginManager
    from media_manager.startup.Installer import Installer
except ImportError:
    from mainuserinterfaces.MainGUI import MainGUI
    from mainuserinterfaces.MainTkGui import MainTkGui
    from plugins.PluginManager import PluginManager
    from startup.Installer import Installer

try:
    # noinspection PyUnresolvedReferences
    import gi
    gi.require_version('Gtk', '3.0')
    # noinspection PyUnresolvedReferences
    from gi.repository import Gtk
    main_gui = MainGUI
except ImportError:
    main_gui = MainTkGui


def main():
    """
    Main method that runs the program
    :return: void
    """

    if not Installer().is_installed():
        Installer().install()

    # ConfigParsing
    config = configparser.ConfigParser()
    config.read(os.getenv("HOME") + "/.mediamanager/configs/mainconfig")
    plugin_config = dict(config.items("plugins"))
    active_plugins = PluginManager(plugin_config).get_plugins()

    # Test tk
    main_gui = MainTkGui
    # Start the program
    gui = main_gui(active_plugins)
    gui.start()

if __name__ == '__main__':
    main()
