from plugins.genericPlugin.GenericPlugin import GenericPlugin
from plugins.folderCreator.userinterfaces.FolderCreatorCLI import FolderCreatorCLI
from plugins.folderCreator.userinterfaces.FolderCreatorGUI import FolderCreatorGUI

"""
Class that handles calls to the FolderCreator class
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class FolderCreatorPlugin(GenericPlugin):

    """
    @:return "Folder Creator"
    """
    def getName(self):
        return "Folder Creator"

    """
    @:return "foldercreator"
    """
    def getCommandName(self):
        return "foldercreator"

    """
    @:return "foldercreator"
    """
    def getConfigTag(self):
        return "foldercreator"

    """
    Starts the CLI of the plugin
    """
    def startCLI(self, parentCLI):
        FolderCreatorCLI().start()

    """
    Starts the GUI of the plugin
    """
    def startGUI(self, parentGUI):
        FolderCreatorGUI(parentGUI).start()