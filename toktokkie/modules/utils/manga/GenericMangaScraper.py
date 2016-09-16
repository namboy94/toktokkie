"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

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
LICENSE
"""

# imports
from typing import List
from toktokkie.modules.objects.manga.MangaVolume import MangaVolume


class GenericMangaScraper(object):
    """
    Class that models how a Manga Scraper should operate
    """

    @staticmethod
    def url_match(manga_url: str) -> bool:
        """
        Checks if a URL matches the pattern expected by the scraper

        :param manga_url: the URL to check
        :return: True if it matches, False otherwise
        """
        raise NotImplementedError()

    @staticmethod
    def scrape_volumes_from_url(manga_url) -> List[MangaVolume]:
        """
        Scrapes a given URL

        :param manga_url: the given URL to scrape
        :return: a list of volumes, which should also contain chapters
        """
        raise NotImplementedError()
