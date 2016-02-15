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
Wrapper for Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes's XDCC Downloader
The plan is to replace his script with one of my own once twisted supports python 3.
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class TwistedDownloader(object):

    """
    Constructor
    @:param packs - the packs to be downloaded
    @:param showName - the show name for auto renaming
    @:param episodeNumber - the (starting) episode number for auto renaming
    @:param seasonNumber - the season number for auto renaming
    """
    def __init__(self, packs, showName="", episodeNumber=0, seasonNumber=0):
        self.packs = packs
        self.autorename = False
        if showName and episodeNumber > 0 and seasonNumber > 0:
            self.showName = showName
            self.episodeNumber = episodeNumber
            self.seasonNumber = seasonNumber
            self.autorename = True

    """
    Starts the Download loop
    """
    def downloadLoop(self):
        for pack in self.packs:
            self.download(pack)

    """
    Downloads a single pack
    """
    def download(self, pack):
        #TODO Look at Hexchatdownloader
        script = os.getenv("HOME") + "/.mediamanager/scripts/xdccbot.py"
        #TODO Get bot name from config
        Popen(["python2", "script", pack.server, pack.channel, "aajajajajjajaja", pack.bot, str(pack.packnumber)])
        if self.autorename:
            #TODO read download path from config
            Episode("", self.showName, self.episodeNumber, self.seasonNumber).rename()
            self.episodeNumber += 1
