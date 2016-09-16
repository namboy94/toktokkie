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
from toktokkie.modules.objects.manga.MangaPage import MangaPage


class MangaChapter(object):
    """
    Class that models a Chapter of the manga

    Contains download links to the individual chapter pages
    """

    pages = []
    """
    The individual pages of the chapter
    """

    chapter_number = -1.0
    """
    The chapter's chapter number
    Is a float to allow chapters like 5.5 or the like
    """

    def __init__(self, chapter_number: float, pages: List[MangaPage]) -> None:
        """
        Initializes a Manga chapter with the contained pages.

        :param chapter_number: The chapter number of this chapter
        :param pages: the chapter pages as list of MangaPage objects
        :return: None
        """
        self.chapter_number = chapter_number
        self.pages = pages
