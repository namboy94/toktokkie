#!/usr/bin/python3
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
import os
import sys
import configparser
from os.path import expanduser

# This import construct enables the program to be run when installed via
# setuptools as well as portable
try:
    from metadata import Globals
except ImportError:
    from media_manager.metadata import Globals



def main(ui_override: str = "") -> None:
    """
    Main method that runs the program.

    It can be used without parameters, in which case it will start in interactive
    command line mode.

    Other options include using the --gtk or --tk flags to start either a GTK 3- or
    a Tkinter-based graphical user interface. This can also be accomplished by
    passing 'gtk' or 'tk' as the ui_override parameter of the main method.

    Furthermore, the program can be used as a pure non-interactive application.
    The options that are available if used like this can be viewed using the
    --help flag.

    :param ui_override: Can override the program mode programmatically
    :return: None
    """

    # First, the used mode of the program is determined using sys.argv
    cli_mode = False
    cli_arg_mode = False

    # Basic parsing of the arguments, which helps establish in which mode the program
    # should be started
    if (len(sys.argv) > 1 and sys.argv[1] == "--gtk") or ui_override == "gtk":
        # This will select the GTK GUI as the selected framework
        Globals.selected_grid_gui_framework = Globals.gtk3_gui_template
    elif (len(sys.argv) > 1 and sys.argv[1] == "--tk") or ui_override == "tk":
        # This will select the Tkinter GUI as the selected framework
        Globals.selected_grid_gui_framework = Globals.tk_gui_template
    elif len(sys.argv) > 1:
        # This will be the mode for non-interactive CLI use
        cli_arg_mode = True
    else:
        # If this is selected, the program will start in interactive CLI use
        cli_mode = True

    # This import has to happen at this point, since the graphical frameworks from
    # gfworks have not been defined correctly in the Globals class before this.
    try:
        from plugins.PluginManager import PluginManager
        from mainuserinterfaces.MainGui import MainGui
        from mainuserinterfaces.MainCli import MainCli
        from mainuserinterfaces.MainArgsParser import MainArgsParser
        from startup.Installer import Installer
    except ImportError:
        from media_manager.plugins.PluginManager import PluginManager
        from media_manager.mainuserinterfaces.MainGui import MainGui
        from media_manager.mainuserinterfaces.MainCli import MainCli
        from media_manager.mainuserinterfaces.MainArgsParser import MainArgsParser
        from media_manager.startup.Installer import Installer

    # This checks if the program is already correctly installed in the user's
    # home directory, if this is not the case the program will be installed now.
    if not Installer.is_installed():
        Installer.install()

    # This parses the config file located in the user's home directory to establish
    # which plugins should be run.
    config = configparser.ConfigParser()
    config.read(os.path.join(expanduser('~'), ".mediamanager", "configs", "mainconfig"))
    plugin_config = dict(config.items("plugins"))
    active_plugins = PluginManager(plugin_config).get_plugins()

    # The program starts here, using the selected mode
    if cli_mode:
        MainCli(active_plugins).start()
    elif cli_arg_mode:
        MainArgsParser(active_plugins).run()
    else:
        gui = MainGui(active_plugins)
        gui.start()

# This executes the main method
if __name__ == '__main__':
    # Keyboard Interrupts are caught and display a farewell message when they occur.
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for using media-manager!")
        sys.exit(0)
