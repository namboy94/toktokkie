import os
from subprocess import Popen

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
        self.mainConfig = self.configDir + "/mainconfig"

    """
    Checks if the program is installed
    @:return True is it is installed, False if not
    """
    def isInstalled(self):
        if not os.path.isdir(self.programDir): return False
        if not os.path.isdir(self.configDir): return False
        if not os.path.isfile(self.mainConfig): return False
        return True

    """
    Installs the program
    """
    def install(self):
        if not os.path.isdir(self.programDir): Popen(["mkdir", self.programDir])
        if not os.path.isdir(self.configDir): Popen(["mkdir", self.configDir])
        if not os.path.isfile(self.mainConfig): self.__writeMainConfig__()

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
