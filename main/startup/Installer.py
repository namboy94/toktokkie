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
        self.programDir = os.getenv("HOME") + "/.mediamanager"
        self.configDir = self.programDir + "/configs"
        self.scriptDir = self.programDir + "/scripts"
        self.mainConfig = self.configDir + "/mainconfig"
        self.xdccDLScript = self.scriptDir + "/xdccbot.py"

    """
    Checks if the program is installed
    @:return True is it is installed, False if not
    """
    def isInstalled(self):
        if not os.path.isdir(self.programDir): return False
        if not os.path.isdir(self.configDir): return False
        if not os.path.isdir(self.scriptDir): return False
        if not os.path.isfile(self.mainConfig): return False
        if not os.path.isfile(self.xdccDLScript): return False
        return True

    """
    Installs the program
    """
    def install(self):
        if not os.path.isdir(self.programDir): Popen(["mkdir", self.programDir])
        if not os.path.isdir(self.configDir): Popen(["mkdir", self.configDir])
        if not os.path.isdir(self.scriptDir): Popen(["mkdir", self.scriptDir])
        if not os.path.isfile(self.mainConfig): self.__writeMainConfig__()
        if not os.path.isfile(self.xdccDLScript): self.__copyXDCCScriptFile__()

    """
    Writes a default config file
    """
    def __writeMainConfig__(self):
        Popen(["touch", self.mainConfig])
        file = open(self.mainConfig, "w")
        file.write("[interface]\n")
        file.write("gui = False\n\n")
        file.write("[plugins]\n")
        file.write("renamer = True\n")
        file.close()

    def __copyXDCCScriptFile__(self):
        original = os.path.dirname(sys.argv[0]) + "/external/xdccbot.py"
        Popen(["cp", original, self.xdccDLScript])
