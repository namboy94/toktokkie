"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a progam that allows convenient managing of various
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
import sys

from mainuserinterfaces.MainCLI import MainCLI
from mainuserinterfaces.MainGUI import MainGUI
from parsers.ArgumentParser import ArgumentParser
from plugins.PluginManager import PluginManager
from startup.Installer import Installer

"""
Main Module that starts the program
@author Hermann Krumrey<hermann@krumreyh.com>
"""

#Parse Arguments
args = ArgumentParser().parse()

#Installation and Updating
if args.install:
    Installer().install()
    sys.exit(0)
if args.update:
    sys.exit(0)

if not Installer().isInstalled():
    print("Program not installed correctly. Install with --install option")
    sys.exit(1)

#ConfigParsing
config = configparser.ConfigParser()
config.read(os.getenv("HOME") + "/.mediamanager/configs/mainconfig")
pluginConfig = dict(config.items("plugins"))
activePlugins = PluginManager(pluginConfig).getPlugins()

#Start the program
if args.gui:
    gui = MainGUI(activePlugins)
    gui.start()
else:
    cli = MainCLI(activePlugins)
    cli.start()