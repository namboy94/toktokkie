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
import shutil
from subprocess import Popen, PIPE
from os.path import expanduser

try:
    from plugins.renamer.objects.Episode import Episode
    from external.xdccbot import get_file_loc
    from plugins.common.calc.FileSizeCalculator import FileSizeCalculator
except ImportError:
    from media_manager.plugins.renamer.objects.Episode import Episode
    from media_manager.external.xdccbot import get_file_loc
    from media_manager.plugins.common.calc.FileSizeCalculator import FileSizeCalculator


class TwistedDownloader(object):
    """
    Wrapper for Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes's XDCC Downloader
    The plan is to replace his script with one of my own once twisted supports python 3.
    """
    
    def __init__(self, packs, progress_struct, show_name="", episode_number=0, season_number=0):
        """
        Constructor
        :param packs: the packs to be downloaded
        :param progress_struct: Structure that keeps track of download progress
        :param show_name: the show name for auto renaming
        :param episode_number: the (starting) episode number for auto renaming
        :param season_number: the season number for auto renaming
        :return: void
        """
        self.packs = packs
        self.progress_struct = progress_struct
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
        files = []
        for pack in self.packs:
            self.progress_struct.single_size = FileSizeCalculator.get_byte_size_from_string(pack.size)
            files.append(self.download(pack))
            self.progress_struct.total_progress += 1
        return files

    def download(self, pack):
        """
        Downloads a single pack
        :param pack: the pack to download
        :return void
        """
        script = os.path.join(expanduser('~'), ".mediamanager", "scripts", "xdccbot.py")
        dl_folder = os.path.join(expanduser('~'), "Downloads")
        if os.path.isfile(script):
            os.remove(script)
        shutil.copy(get_file_loc(), script)

        dl_command = ["python2",
                      script,
                      pack.server,
                      pack.channel.split("#", 1)[1],
                      "media_manager_python",
                      pack.bot,
                      dl_folder,
                      str(pack.packnumber)]

        proc = Popen(dl_command, stderr=PIPE)
        file_name = ""
        while True:
            line = proc.stderr.readline().decode().split("\n")[0]
            if "PROGRESS:" in line:
                print("PROGRESS" + line.split("PROGRESS")[1])
                self.progress_struct.single_progress = int(line.split("PROGRESS:")[1])
            elif "DLCOMPLETE:" in line:
                print(line)
                file_name = line.split("DLCOMPLETE:")[1]
            elif not line:
                break
        if not file_name:
            raise Exception("Twisted Download Error")

        file_path = os.path.join(dl_folder, file_name)

        if self.auto_rename:
            episode = Episode(file_path, self.episode_number, self.season_number, self.show_name)
            episode.rename()
            self.episode_number += 1
            return episode.episode_file
        else:
            return file_path
