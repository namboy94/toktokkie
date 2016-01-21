import os
from subprocess import Popen

import sys

"""
Class that handles installation of the program
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class Installer(object):

    """
    Constructor
    """
    def __init__(self):
        self.mainDir = os.getenv("HOME") + "/.mediamanager"
        self.configDir = self.mainDir + "/configs"
        self.scriptDir = self.mainDir + "/scripts"
        self.mainConfig = self.configDir + "/mainconfig"
        self.xdccDLScript = self.scriptDir + "/xdccbot.py"
        self.programDir = self.mainDir + "/program"
        self.executable = "/usr/bin/mediamanager"
        self.guiExecutable = "/usr/bin/mmgui"

    """
    Checks if the program is installed
    @:return True is it is installed, False if not
    """
    def isInstalled(self):
        if not os.path.isdir(self.mainDir): return False
        if not os.path.isdir(self.configDir): return False
        if not os.path.isdir(self.scriptDir): return False
        if not os.path.isfile(self.mainConfig): return False
        if not os.path.isfile(self.xdccDLScript): return False
        if not os.path.isdir(self.programDir): return False
        if not os.path.isfile(self.executable): return False
        if not os.path.isfile(self.guiExecutable): return False
        return True

    """
    Installs the program
    """
    def install(self):
        if not os.path.isdir(self.mainDir): Popen(["mkdir", self.mainDir]).wait()
        if not os.path.isdir(self.configDir): Popen(["mkdir", self.configDir]).wait()
        if not os.path.isdir(self.scriptDir): Popen(["mkdir", self.scriptDir]).wait()
        if not os.path.isfile(self.mainConfig): self.__writeMainConfig__()
        if not os.path.isfile(self.xdccDLScript): self.__copyXDCCScriptFile__()
        if not os.path.isdir(self.programDir): Popen(["cp", "-rf", Installer.getSourceDir(), self.programDir]).wait()
        if not os.path.isfile(self.executable):
            Popen(["sudo", "cp", Installer.getSourceDir() + "/main/startup/scripts/mediamanagercli.sh", self.executable]).wait()
            Popen(["sudo", "chmod", "755", self.executable]).wait()
        if not os.path.isfile(self.guiExecutable):
            Popen(["sudo", "cp", Installer.getSourceDir() + "/main/startup/scripts/mediamanagergui.sh", self.guiExecutable]).wait()
            Popen(["sudo", "chmod", "755", self.guiExecutable]).wait()

    """
    Writes a default config file
    """
    def __writeMainConfig__(self):
        Popen(["touch", self.mainConfig])
        file = open(self.mainConfig, "w")
        file.write("[plugins]\n")
        file.write("renamer = True\n")
        file.write("xdcc-searchdownload = True\n")
        file.write("\n[defaults]\n")
        file.write("downloader = twisted\n#options = (twisted|hexchat)\n")
        file.close()

    """
    Copies the xdcc download script to the program directory.
    THis has to be done differently once twisted's irc module is ported to python 3
    """
    def __copyXDCCScriptFile__(self):
        original = os.path.dirname(sys.argv[0]) + "/external/xdccbot.py"
        Popen(["cp", original, self.xdccDLScript]).wait()


    """
    Gets the source directory of the python program running
    @:return the source directory
    """
    @staticmethod
    def getSourceDir():
        directory = os.path.dirname(sys.argv[0])
        return str(os.path.abspath(directory).rsplit("/", 1)[0])