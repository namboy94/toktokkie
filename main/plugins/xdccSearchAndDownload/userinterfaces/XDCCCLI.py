import configparser
from plugins.genericPlugin.userinterfaces.GenericCLI import GenericCLI
from plugins.xdccSearchAndDownload.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
from plugins.xdccSearchAndDownload.downloaders.TwistedDownloader import TwistedDownloader
from plugins.xdccSearchAndDownload.searchers.NIBLGetter import NIBLGetter

"""
CLI for the XDCC Search and Download plugin
@author Hermann Krumrey <hermann@krumreyh.com>
"""
class XDCCCLI(GenericCLI):

    """
    Constructor
    """
    def __init__(self):
        print()

    """
    Starts the CLi
    """
    def start(self):
        print("Currently Unsupported in a non-GUI environment, sorry!")