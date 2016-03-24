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
import sys
import configparser
from os.path import expanduser

try:
    from startup.Installer import Installer
    from Globals import Globals
except ImportError:
    from media_manager.startup.Installer import Installer
    from media_manager.Globals import Globals


def main(ui_override="gtk"):
    """
    Main method that runs the program
    :return: void
    """

    if not Installer().is_installed():
        Installer().install()

    # Parse arguments
    if (len(sys.argv) > 1 and sys.argv[1] == "--gtk") or ui_override == "gtk":
        Globals.selected_grid_gui_framework = Globals.gtk3_gui_template
    elif (len(sys.argv) > 1 and sys.argv[1] == "--tk") or ui_override == "tk":
        Globals.selected_grid_gui_framework = Globals.tk_gui_template
    else:
        print("No valid GUI framework specified. Please use either --gtk or --tk")
        sys.exit(1)

    try:
        from plugins.PluginManager import PluginManager
        from mainuserinterfaces.MainGUI import MainGUI
    except ImportError:
        from media_manager.plugins.PluginManager import PluginManager
        from media_manager.mainuserinterfaces.MainGUI import MainGUI

    # ConfigParsing
    config = configparser.ConfigParser()
    config.read(os.path.join(expanduser('~'), ".mediamanager", "configs", "mainconfig"))
    plugin_config = dict(config.items("plugins"))
    active_plugins = PluginManager(plugin_config).get_plugins()

    # Start the program
    gui = MainGUI(active_plugins)
    gui.start()

if __name__ == '__main__':
    main()
