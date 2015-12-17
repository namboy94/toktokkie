from mainuserinterfaces.MainGUI import MainGUI
from plugins.genericPlugin.GenericPlugin import GenericPlugin
from plugins.xdccSearchAndDownload.userinterfaces.XDCCGUI import XDCCGUI
from plugins.xdccSearchAndDownload.userinterfaces.XDCCCLI import XDCCCLI

"""
Class that handles renaming of episodes
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class XDCCPlugin(GenericPlugin):

    """
    @:return "Renamer"
    """
    def getName(self):
        return "XDCC-Search-Download"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        XDCCCLI().start()

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        parentGUI.root.destroy()
        XDCCGUI().start()