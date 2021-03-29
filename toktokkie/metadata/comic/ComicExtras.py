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
from abc import ABC
from typing import List
from toktokkie.metadata.base.MetadataBase import MetadataBase


class ComicExtras(MetadataBase, ABC):
    """
    Additional methods and attributes for comic metadata objects
    """

    @property
    def main_chapters_path(self) -> str:
        """
        The path to the main manga directory containing chapters
        :return: The path
        """
        return os.path.join(self.directory_path, "Chapters")

    @property
    def main_volumes_path(self) -> str:
        """
        The path to the main manga directory containing volumes
        :return: The path
        """
        return os.path.join(self.directory_path, "Volumes")

    @property
    def special_path(self) -> str:
        """
        The path to the special manga directory
        :return: The path or None if it does not exist
        """
        return os.path.join(self.directory_path, "Special")

    @property
    def special_chapters(self) -> List[str]:
        """
        :return: A list of special chapter identifiers for this series
        """
        return self.json.get("special_chapters", [])

    @special_chapters.setter
    def special_chapters(self, special_chapters: List[str]):
        """
        Setter method for the special_chapters
        :param special_chapters: The special chapter identifiers to set
        :return: None
        """
        if len(special_chapters) > 0:
            max_len = len(max(special_chapters, key=lambda x: len(x)))
            special_chapters.sort(key=lambda x: x.zfill(max_len))
        self.json["special_chapters"] = special_chapters

    @property
    def chapter_offset(self) -> int:
        """
        :return: The chapter offset if the chapters don't start at 1
        """
        return self.json.get("chapter_offset", 0)

    @chapter_offset.setter
    def chapter_offset(self, offset: int):
        """
        Sets the chapter offset
        :param offset: The chapter offset
        :return: None
        """
        self.json["chapter_offset"] = offset
