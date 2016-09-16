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
import requests
from bs4 import BeautifulSoup
from typing import List
from toktokkie.modules.objects.manga.MangaPage import MangaPage
from toktokkie.modules.objects.manga.MangaVolume import MangaVolume
from toktokkie.modules.objects.manga.MangaChapter import MangaChapter
from toktokkie.modules.utils.manga.GenericMangaScraper import GenericMangaScraper


class MangaFoxScraper(GenericMangaScraper):
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
        return manga_url.startswith("http://mangafox.me")

    @staticmethod
    def scrape_volumes_from_url(manga_url) -> List[MangaVolume]:
        """
        Scrapes a given URL

        :param manga_url: the given URL to scrape
        :return: a list of volumes, which should also contain chapters
        """

        html = requests.get(manga_url).text
        soup = BeautifulSoup(html, "html.parser")
        volumes = soup.select(".chlist")

        # Find the highest volume number
        # Sometimes a 'Volume 00' exists, which then results in us having to decrement the
        # highest number by 1
        volume_number = len(volumes)
        if "\"Volume 00\"" in html:
            volume_number -= 1

        volume_objects = []

        for volume in volumes:
            chapters = volume.select(".tips")

            chapter_objects = []

            for chapter in chapters:
                chapter_start_url = str(chapter).split("href=\"")[1].split("\"")[0]
                chapter_base_url = chapter_start_url.rsplit("/", 1)[0]
                chapter_number = float(chapter.text.rsplit(" ", 1)[1])

                chapter_html = requests.get(chapter_start_url).text
                chapter_soup = BeautifulSoup(chapter_html, "html.parser")
                page_amount = int(str(chapter_soup.select(".l")[0]).rsplit("of ", 1)[1].split("\t", 1)[0])  # Don't ask

                page_objects = []

                for image_number in range(1, page_amount + 1):

                    print(image_number)

                    image_page_url = chapter_base_url + "/" + str(image_number) + ".html"
                    image_html = requests.get(image_page_url).text
                    image_soup = BeautifulSoup(image_html, "html.parser")

                    image = image_soup.select("img")[0]
                    image_url = str(image).split("src='")[1].split("'")[0]

                    page_objects.append(MangaPage(image_number, image_url))

                chapter_objects.append(MangaChapter(chapter_number, page_objects))

            volume_objects.append(MangaVolume(volume_number, chapter_objects))

        return volume_objects
