import configparser
import os
import sys

from mainuserinterfaces.MainCLI import MainCLI
from mainuserinterfaces.MainGUI import MainGUI
from parsers.ArgumentParser import ArgumentParser
from plugins.PluginManager import PluginManager
from startup.Installer import Installer

args = ArgumentParser().parse()

if args.install:
    Installer().install()
    sys.exit(0)
if args.update:
    sys.exit(0)

config = configparser.ConfigParser()
config.read(os.getenv("HOME") + "/.mediamanager/configs/mainconfig")
pluginConfig = dict(config.items("plugins"))
activePlugins = PluginManager(pluginConfig).getPlugins()

if not Installer().isInstalled():
    print("Program not installed correctly. Install with --install option")
    sys.exit(1)

if config.get("interface", "gui").lower() in ["true", "1", "yes"]:
    gui = MainGUI(activePlugins)
    gui.start()
else:
    cli = MainCLI(activePlugins)
    cli.start()