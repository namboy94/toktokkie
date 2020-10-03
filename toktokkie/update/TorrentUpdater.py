"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

This file is part of toktokkie.

toktokkie is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

toktokkie is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import time
import shutil
from typing import List, Dict, Set
from qbittorrent import Client
from toktokkie.update.TvUpdater import TvUpdater, DownloadInstructions
from toktokkie.torrent.search import search_engines
from toktokkie.torrent.search.SearchEngine import SearchEngine
from toktokkie.torrent.search.TorrentInfo import TorrentInfo
from toktokkie.Config import Config


class TorrentUpdater(TvUpdater):
    """
    Class that handles the configuration and execution of an xdcc update
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the Updater
        """
        return "torrent"

    @classmethod
    def search_engine_names(cls) -> Set[str]:
        """
        :return: The names of applicable search engines
        """
        return {x.name() for x in search_engines}

    @property
    def search_engine(self) -> SearchEngine:
        """
        :return: The search engine to use
        """
        return {
            x.name(): x for x in search_engines
        }[self.config["search_engine"]]()

    @classmethod
    def predefined_patterns(cls) -> Dict[str, str]:
        """
        :return: Predefined search patterns for this updater
        """
        return {
            "erai-raws": "[Erai-raws] @{NAME} - @{EPI-2} "
                         "[@{RES-P}]@{ANY}.mkv"
        }

    def download(self, download_instructions: List[DownloadInstructions]):
        """
        Performs a download
        :param download_instructions: The download instrcutions
        :return: None
        """
        url, user, password, torrent_dir = Config().qbittorrent_config
        client = Client(url)
        client.login(user, password)

        for instruction in download_instructions:

            torrent_info: TorrentInfo = instruction.search_result
            destination_path = \
                os.path.join(instruction.directory, instruction.filename)

            print(f"Downloading Torrent: {torrent_info.filename}")

            client.download_from_link(torrent_info.magnet_link)
            while len(client.torrents()) > 0:
                for torrent in client.torrents():
                    if torrent["state"] not in [
                        "downloading", "metaDL", "stalledDL"
                    ]:
                        print("Done.     ")
                        torrent_path = os.path.join(torrent_dir,
                                                    torrent["name"])

                        if os.path.isdir(torrent_path):
                            children = [
                                os.path.join(torrent_path, x)
                                for x in os.listdir(torrent_path)
                            ]
                            children.sort(
                                key=lambda x: os.path.getsize(x), reverse=True
                            )
                            torrent_path = children[0]
                            ext = torrent_path.rsplit(".", 1)[1]
                            destination_path += "." + ext

                        client.delete(torrent["hash"])
                        shutil.move(torrent_path, destination_path)
                    else:
                        print(f"{(100 * torrent['progress']):.2f}%", end="\r")

                time.sleep(1)
