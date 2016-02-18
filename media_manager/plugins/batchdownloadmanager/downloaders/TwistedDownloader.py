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

from subprocess import Popen

try:
    from media_manager.plugins.renamer.objects.Episode import Episode
except ImportError:
    from plugins.renamer.objects.Episode import Episode


class TwistedDownloader(object):
    """
    Wrapper for Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes's XDCC Downloader
    The plan is to replace his script with one of my own once twisted supports python 3.
    """
    
    def __init__(self, packs, show_name="", episode_number=0, season_number=0):
        """
        Constructor
        :param packs: the packs to be downloaded
        :param show_name: the show name for auto renaming
        :param episode_number: the (starting) episode number for auto renaming
        :param season_number: the season number for auto renaming
        :return: void
        """
        self.packs = packs
        self.auto_rename = False
        if show_name and episode_number > 0 and season_number > 0:
            self.show_name = show_name
            self.episode_number = episode_number
            self.season_number = season_number
            self.auto_rename = True

    def download_loop(self):
        """
        Starts the Download loop
        :return void
        """
        for pack in self.packs:
            self.download(pack)

    # TODO Implement
    def download(self, pack):
        """
        Downloads a single pack
        :param pack: the pack to download
        :return void
        """
        # TODO Look at Hexchatdownloader
        #
        # script = os.getenv("HOME") + "/.mediamanager/scripts/xdccbot.py"
        # TODO Get bot name from config
        Popen(["python2", "script", pack.server, pack.channel, "", pack.bot, str(pack.packnumber)])
        if self.auto_rename:
            # TODO read download path from config
            Episode("", self.show_name, self.episode_number, self.season_number).rename()
            self.episode_number += 1
