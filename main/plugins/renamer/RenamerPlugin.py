from mainuserinterfaces.MainGUI import MainGUI
from plugins.genericPlugin.GenericPlugin import GenericPlugin
from plugins.renamer.userinterface.RenamerGUI import RenamerGUI
from plugins.renamer.userinterface.RenamerCLI import RenamerCLI

"""
Class that handles renaming of episodes
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class RenamerPlugin(GenericPlugin):

    """
    @:return "Renamer"
    """
    def getName(self):
        return "Renamer"

    """
    @:return "renamer"
    """
    def getConfigTag(self):
        return "renamer"

    """
    @:return "renamer"
    """
    def getCommandName(self):
        return "renamer"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        RenamerCLI().start()

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        RenamerGUI(parentGUI).start()