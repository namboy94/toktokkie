import os
from subprocess import Popen
"""
Wrapper for Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes's XDCC Downloader
The plan is to replace his script with one of my own once twisted supports python 3.
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class TwistedDownloader(object):

    """
    Constructor
    """
    def __init__(self, packs):
        self.packs = packs

    """
    Starts the Download loop
    """
    def downloadLoop(self):
        for pack in self.packs:
            TwistedDownloader.download(pack)

    """
    Downloads a single pack
    """
    @staticmethod
    def download(pack):
        script = os.getenv("HOME") + "/.mediamanager/scripts/xdccbot.py"
        Popen(["python2", "script", pack.server, pack.channel, "aajajajajjajaja", pack.bot, str(pack.packnumber)])