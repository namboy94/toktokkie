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


class MangaPage(object):
    """
    Class that models a page in a Manga chapter
    """

    page_number = -1
    """
    The page's page number
    """

    image_url = ""
    """
    The URL to the page's image
    """

    def __init__(self, page_number: int, image_url: str) -> None:
        """
        Initializes the Manga Page with a page number and an image URL

        :param page_number: the page number
        :param image_url: the image URL
        :return: None
        """
        self.page_number = page_number
        self.image_url = image_url
