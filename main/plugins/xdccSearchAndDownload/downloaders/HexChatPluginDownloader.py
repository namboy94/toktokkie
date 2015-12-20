"""
XDCC Downloader that makes use of Hexchat's python scripting interface
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class HexChatPluginDownloader(object):

    def __init__(self, packs):
        self.packs = packs