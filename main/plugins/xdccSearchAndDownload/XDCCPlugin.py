from plugins.genericPlugin.GenericPlugin import GenericPlugin
from plugins.xdccSearchAndDownload.userinterfaces.XDCCGUI import XDCCGUI
from plugins.xdccSearchAndDownload.userinterfaces.XDCCCLI import XDCCCLI

"""
Class that handles renaming of episodes
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class XDCCPlugin(GenericPlugin):

    """
    @:return "XDCC-Search-Download"
    """
    def getName(self):
        return "XDCC-Search-Download"

    """
    @:return "xdcc-searchdownload"
    """
    def getConfigTag(self):
        return "xdcc-searchdownload"

    """
    @:return "xdcc-searchdl"
    """
    def getCommandName(self):
        return "xdcc-searchdl"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        XDCCCLI().start()

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        XDCCGUI(parentGUI, "XDCC Search and Download").start()
