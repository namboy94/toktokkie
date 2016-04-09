"""
LICENSE:

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

LICENSE
"""

import os
import time
import platform

from subprocess import Popen
from threading import Thread

try:
    from plugins.renamer.objects.Episode import Episode
    from plugins.common.calc.FileSizeCalculator import FileSizeCalculator
except ImportError:
    from media_manager.plugins.renamer.objects.Episode import Episode
    from media_manager.plugins.common.calc.FileSizeCalculator import FileSizeCalculator


class HexChatPluginDownloader(object):
    """
    XDCC Downloader that makes use of Hexchat's python scripting interface
    """

    def __init__(self, packs, progress_struct, show_name="", episode_number=0, season_number=0):
        """
        Constructor
        :param packs: the packs to be downloaded
        :param progress_struct: Structure to keep track of download progress
        :param show_name: the show name for use with auto_rename
        :param episode_number: the (first) episode number for use with auto_rename
        :param season_number: the season number for use with auto_rename
        :return: void
        """
        if platform.system() == "Linux":
            self.script_location = os.path.join(os.path.expanduser('~'), ".config", "hexchat", "addons", "dlscript.py")
            self.hexchat_config_location = os.path.join(os.path.expanduser('~'), ".config", "hexchat", "hexchat.conf")
        elif platform.system() == "Windows":
            self.script_location = os.path.join(os.path.expanduser('~'),
                                                "AppData", "Roaming", "HexChat", "addons", "dlscript.py")
            self.hexchat_config_location = os.path.join(os.path.expanduser('~'),
                                                        "AppData", "Roaming", "HexChat", "hexchat.conf")
        self.packs = packs
        self.progress_struct = progress_struct
        self.downloading = False
        self.script = open(self.script_location, 'w')
        self.download_dir = ""

        hexchat_config = open(self.hexchat_config_location, 'r')
        content = hexchat_config.read()
        hexchat_config.close()
        new_content = []
        for line in content.split("\n"):
            if "gui_join_dialog" in line:
                new_content.append("gui_join_dialog = 0")
            elif "dcc_auto_recv" in line:
                new_content.append("dcc_auto_recv = 2")
            elif "gui_slist_skip" in line:
                new_content.append("gui_slist_skip = 1")
            elif "dcc_dir = " in line:
                self.download_dir = line.split("dcc_dir = ")[1].split("\n")[0]
                new_content.append(line)
            else:
                new_content.append(line)
        new_content.pop()

        # TODO get this to work on Windows
        if platform.system() == "Linux":
            hexchat_config = open(self.hexchat_config_location, 'w')
            for line in new_content:
                hexchat_config.write(line + "\n")
            hexchat_config.close()

        self.auto_rename = False
        if show_name and episode_number > 0 and season_number > 0:
            self.auto_rename = True
            self.show_name = show_name
            self.episode_number = int(episode_number)
            self.season_number = int(season_number)

    def __write_start__(self):
        """
        Writes the beginning of the downloader script
        :return: void
        """
        script_start = ["__module_name__ = \"xdcc_executer\"",
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
        for line in script_start:
            self.script.write(line + "\n")

    def __write_end__(self):
        """
        Writes the end of the downloader script
        :return: void
        """
        script_end = ["hexchat.command(channels[0])",
                      "hexchat.hook_print(\"You Join\", download)",
                      "hexchat.hook_print(\"DCC RECV Complete\", downloadComplete)",
                      "hexchat.hook_print(\"DCC STALL\", downloadFailed)",
                      "hexchat.hook_print(\"DCC RECV Abort\", downloadFailed)",
                      "hexchat.hook_print(\"DCC RECV Failed\", downloadFailed)",
                      "hexchat.hook_print(\"DCC Timeout\", downloadFailed)"]
        for line in script_end:
            self.script.write(line + "\n")

    def __write_script__(self, pack):
        """
        Writes the downloader script
        :return: void
        """
        self.__write_start__()
        self.script.write("channels.append(\"newserver irc://" + pack.server + "/" + pack.channel + "\")\n")
        self.script.write("packs.append(\"msg " + pack.bot + " xdcc send #" + str(pack.packnumber) + "\")\n")
        self.__write_end__()
        self.script.close()

    def download_loop(self):
        """
        Starts the download loop
        :return a list of file paths leading to the downloaded files
        """
        downloaded = []

        for pack in self.packs:
            self.download_single(pack)

        self.packs.sort(key=lambda x: x.filename)

        if self.auto_rename:
            for pack in self.packs:
                episode = Episode(os.path.join(self.download_dir, pack.filename),
                                  self.episode_number, self.season_number, self.show_name)
                episode.rename()
                downloaded.append(episode.episode_file)
                self.episode_number += 1
        else:
            for pack in self.packs:
                downloaded.append(os.path.join(self.download_dir, pack.filename))
        return downloaded

    def download_single(self, pack):
        self.progress_struct.single_size = FileSizeCalculator.get_byte_size_from_string(pack.size)
        progress_thread = Thread(target=self.update_progress, args=(pack,))

        self.__write_script__(pack)
        self.downloading = True
        progress_thread.start()

        if platform.system() == "Linux":
            Popen(["hexchat"]).wait()
        elif platform.system() == "Windows":
            if os.path.isfile("C:\\Program Files\\HexChat\\hexchat.exe"):
                Popen(["C:\\Program Files\\HexChat\\hexchat.exe"]).wait()
        self.downloading = False
        self.progress_struct.total_progress += 1
        os.remove(self.script_location)

    def update_progress(self, pack):
        while self.downloading:
            try:
                self.progress_struct.single_progress = os.path.getsize(os.path.join(self.download_dir, pack.filename))
            except os.error:
                self.progress_struct.single_progress = 0
            time.sleep(1)
        self.progress_struct.single_progress = 0
        self.progress_struct.single_size = 0


