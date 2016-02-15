"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.
"""

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
                    self.downloaddir = line.split("dcc_dir = ")[1].split("\n")[0]
                    if not self.downloaddir.endswith("/"): self.downloaddir += "/"
                    break
            hexchatconfig.close()

    """
    Writes the beginning of the downloader script
    """
    def __writestart__(self):
        scriptstart = ["__module_name__ = \"xdcc_executer\"",
                         "__module_version__ = \"1.0\"",
                         "__module_description__ = \"Python XDCC Executer\"\n",
                         "import hexchat",
                         "import sys\n",
                         "def download(word, word_eol, userdata):",
                         "\thexchat.command(packs[0])",
                         "\treturn hexchat.EAT_HEXCHAT\n",
                         "def downloadComplete(word, word_eol, userdata):",
                         "\thexchat.command('quit')",
                         "\tchannels.pop(0)",
                         "\tpacks.pop(0)",
                         "\tif len(channels) == 0:",
                         "\t\tsys.exit(1)",
                         "\telse:",
                         "\t\thexchat.command(channels[0])",
                         "\treturn hexchat.EAT_HEXCHAT\n",
                         "def downloadFailed(word, word_eol, userdata):",
                         "\tfailed.append(packs[0])",
                         "\thexchat.command('quit')",
                         "\tchannels.pop(0)",
                         "\tpacks.pop(0)",
                         "\tif len(channels) == 0:",
                         "\t\tsys.exit(1)",
                         "\telse:",
                         "\t\thexchat.command(channels[0])",
                         "\treturn hexchat.EAT_HEXCHAT\n",
                         "failed = []",
                         "channels = []",
                         "packs = []\n"]
        for line in scriptstart:
            self.script.write(line + "\n")

    """
    Writes the end of the downloader script
    """
    def __writeEnd__(self):
        scriptend = ["hexchat.command(channels[0])",
                       "hexchat.hook_print(\"You Join\", download)",
                       "hexchat.hook_print(\"DCC RECV Complete\", downloadComplete)",
                       "hexchat.hook_print(\"DCC STALL\", downloadFailed)",
                       "hexchat.hook_print(\"DCC RECV Abort\", downloadFailed)",
                       "hexchat.hook_print(\"DCC RECV Failed\", downloadFailed)",
                       "hexchat.hook_print(\"DCC Timeout\", downloadFailed)"]
        for line in scriptend:
            self.script.write(line + "\n")

    """
    Writes the downloader script
    """
    def __writeScript__(self):
        self.__writestart__()
        for pack in self.packs:
            self.script.write("channels.append(\"newserver irc://" + pack.server + "/" + pack.channel + "\")\n")
            self.script.write("packs.append(\"msg " + pack.bot + " xdcc send #" + str(pack.packnumber) + "\")\n")
        self.__writeEnd__()
        self.script.close()

    """
    Starts the download loop
    """
    def downloadLoop(self):
        self.__writeScript__()
        Popen(["hexchat"]).wait()
        downloaded = []
        self.packs.sort(key=lambda x: x.filename)
        if self.autorename:
            for pack in self.packs:
                episode = Episode(self.downloaddir + pack.filename, self.episodeNumber, self.seasonNumber, self.showName)
                episode.rename()
                downloaded.append(episode.episodeFile)
                self.episodeNumber += 1
        else:
            for pack in self.packs:
                downloaded.append(self.downloaddir + pack.filename)
        return downloaded