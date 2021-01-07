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

from typing import List, Dict, Set
from toktokkie.utils.update.TvUpdater import TvUpdater, DownloadInstructions
from torrent_dl.search import search_engines
from torrent_dl.search.SearchEngine import SearchEngine
from torrent_dl.entities.TorrentDownload import TorrentDownload
from torrent_dl.download.QBittorrentDownloader import QBittorrentDownloader


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
                         "@{ANY}[@{RES-P}]@{ANY}.mkv",
            "subsplease": "[SubsPlease] @{NAME} - @{EPI-2} "
                          "(@{RES-P}) [@{HASH}].mkv"
        }

    def download(self, download_instructions: List[DownloadInstructions]):
        """
        Performs a download
        :param download_instructions: The download instrcutions
        :return: None
        """
        downloader = QBittorrentDownloader()
        torrents = [
            TorrentDownload(x.search_result, x.directory, x.filename)
            for x in download_instructions
        ]
        downloader.download(torrents)
