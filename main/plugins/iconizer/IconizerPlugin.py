from plugins.genericPlugin.GenericPlugin import GenericPlugin
from plugins.iconizer.userinterfaces.IconizerCLI import IconizerCLI
from plugins.iconizer.userinterfaces.IconizerGUI import IconizerGUI

"""
Class that handles iconizing of folders
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class IconizerPlugin(GenericPlugin):

    """
    @:return "Iconizer"
    """
    def getName(self):
        return "Iconizer"

    """
    @:return "iconizer"
    """
    def getConfigTag(self):
        return "iconizer"

    """
    @:return "iconizer"
    """
    def getCommandName(self):
        return "iconizer"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        IconizerCLI().start()

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        IconizerGUI(parentGUI, "Folder Iconizer GUI").start()
