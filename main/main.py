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