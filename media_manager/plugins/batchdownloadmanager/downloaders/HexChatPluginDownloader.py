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

try:
    from media_manager.plugins.renamer.objects.Episode import Episode
except ImportError:
    from plugins.renamer.objects.Episode import Episode


class HexChatPluginDownloader(object):
    """
    XDCC Downloader that makes use of Hexchat's python scripting interface
    """

    def __init__(self, packs, show_name="", episode_number=0, season_number=0):
        """
        Constructor
        :param packs: the packs to be downloaded
        :param show_name: the show name for use with auto_rename
        :param episode_number: the (first) episode number for use with auto_rename
        :param season_number: the season number for use with auto_rename
        :return: void
        """
        self.packs = packs
        self.script = open(os.getenv("HOME") + "/.config/hexchat/addons/dlscript.py", 'w')
        self.auto_rename = False
        if show_name and episode_number > 0 and season_number > 0:
            self.auto_rename = True
            self.show_name = show_name
            self.episode_number = int(episode_number)
            self.season_number = int(season_number)
            self.download_dir = ""
            hexchat_config = open(os.getenv("HOME") + "/.config/hexchat/hexchat.conf", 'r')
            for line in hexchat_config:
                if "dcc_dir = " in line:
                    self.download_dir = line.split("dcc_dir = ")[1].split("\n")[0]
                    if not self.download_dir.endswith("/"):
                        self.download_dir += "/"
                    break
            hexchat_config.close()

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

    def __write_script__(self):
        """
        Writes the downloader script
        :return: void
        """
        self.__write_start__()
        for pack in self.packs:
            self.script.write("channels.append(\"newserver irc://" + pack.server + "/" + pack.channel + "\")\n")
            self.script.write("packs.append(\"msg " + pack.bot + " xdcc send #" + str(pack.packnumber) + "\")\n")
        self.__write_end__()
        self.script.close()

    def download_loop(self):
        """
        Starts the download loop
        :return a list of file paths leading to the downloaded files
        """
        self.__write_script__()
        Popen(["hexchat"]).wait()
        downloaded = []
        self.packs.sort(key=lambda x: x.filename)
        if self.auto_rename:
            for pack in self.packs:
                episode = Episode(self.download_dir + pack.filename,
                                  self.episode_number, self.season_number, self.show_name)
                episode.rename()
                downloaded.append(episode.episode_file)
                self.episode_number += 1
        else:
            for pack in self.packs:
                downloaded.append(self.download_dir + pack.filename)
        return downloaded
