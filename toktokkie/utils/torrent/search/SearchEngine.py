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

from typing import List
from toktokkie.utils.torrent.search.TorrentInfo import TorrentInfo


class SearchEngine:
    """
    Specifies the methods a search engine needs to be able to do
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the search engine
        """
        raise NotImplementedError()

    def search(self, search_term) -> List[TorrentInfo]:
        """
        Performs the actual search
        :param search_term: The term to search for
        :return: The search results
        """
        raise NotImplementedError()
