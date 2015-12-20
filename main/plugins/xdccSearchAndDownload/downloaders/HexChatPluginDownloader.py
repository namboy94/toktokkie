import os
from subprocess import Popen
from plugins.renamer.objects.Episode import Episode

"""
XDCC Downloader that makes use of Hexchat's python scripting interface
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class HexChatPluginDownloader(object):

    """
    Constructor
    @:param packs - the packs to be downloaded
    @:param showName - the show name for use with autorename
    @:param episodeNumber - the (first) episode number for use with autorename
    @:param seasonNumber - the season number for use with autorename
    """
    def __init__(self, packs, showName="", episodeNumber=0, seasonNumber=0):
        self.packs = packs
        self.script = open(os.getenv("HOME") + "/.config/hexchat/addons/dlscript.py", 'w')
        self.autorename = False
        if showName and episodeNumber > 0 and seasonNumber > 0:
            self.autorename = True
            self.showName = showName
            self.episodeNumber = int(episodeNumber)
            self.seasonNumber = int(seasonNumber)
            self.downloaddir = ""
            hexchatconfig = open(os.getenv("HOME") + "/.config/hexchat/hexchat.conf", 'r')
            for line in hexchatconfig:
                if "dcc_dir = " in line:
                    self.downloaddir = line.split("dcc_dir = ")[1]
                    break
            hexchatconfig.close()

    """
    Writes the beginning of the downloader script
    """
    def __writestart__(self):
        print()
        #TODO write what comes in the front part of the script

    """
    Writes the end of the downloader script
    """
    def __writeEnd__(self):
        print()
        #TODO write what comes in the end of the script

    """
    Writes the downloader script
    """
    def __writeScript__(self):
        self.__writestart__()
        for pack in self.packs:
            print()
            #TODO write what comes in the middle of the script
        self.__writeEnd__()
        self.script.close()

    """
    Starts the download loop
    """
    def downloadLoop(self):
        self.__writeScript__()
        Popen(["hexchat"])
        if self.autorename:
            for pack in self.packs:
                Episode(self.downloaddir + pack.filename, self.showName, self.episodeNumber, self.seasonNumber).rename()
                self.episodeNumber += 1


