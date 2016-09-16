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

# import
from typing import List
from toktokkie.modules.objects.manga.MangaChapter import MangaChapter


class MangaVolume(object):
    """
    Class that models a Manga chapter.

    Contains a list of chapters
    """

    chapters = []
    """
    List of Manga chapters in this volume
    """

    volume_number = -1
    """
    The volume's Volume Number
    """

    def __init__(self, volume_number: int, chapters: List[MangaChapter]) -> None:
        """
        Initializes a Manga volume with a list of chapters

        :param volume_number: The volume number of this volume
        :param chapters: the chapters belonging to this volume
        :return: None
        """
        self.volume_number = volume_number
        self.chapters = chapters
