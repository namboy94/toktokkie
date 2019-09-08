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
from typing import List, Optional
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.components.enums import MediaType, MangaIdType
from toktokkie.metadata.prompt.CommaList import CommaList
from toktokkie.metadata.helper.wrappers import json_parameter


class Manga(Metadata):
    """
    Metadata class that models a Manga series
    """

    @classmethod
    def id_type(cls) -> type(MangaIdType):
        """
        :return: The ID type used by this metadata object
        """
        return MangaIdType

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        return MediaType.MANGA

    @classmethod
    def prompt(cls, directory_path: str) -> Metadata:
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        print("Generating metadata for {}:"
              .format(os.path.basename(directory_path)))
        series = cls(directory_path, {
            "ids": cls.prompt_for_ids(),
            "type": cls.media_type().value,
            "special_chapters": []
        })

        if series.special_path is not None:
            print("Please enter identifiers for special chapters:")
            for _file in sorted(os.listdir(series.special_path)):
                print(_file)
            series.special_chapters = cls.input(
                "Special Chapters", CommaList(""), CommaList
            ).value
        return series

    @property
    def main_path(self) -> str:
        """
        The path to the main manga directory
        :return: The path
        """
        return os.path.join(self.directory_path, "Main")

    @property
    def special_path(self) -> Optional[str]:
        """
        The path to the special manga directory
        :return: The path or None if it does not exist
        """
        path = os.path.join(self.directory_path, "Special")
        return path if os.path.isdir(path) else None

    @property
    @json_parameter
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
        self.json["special_chapters"] = special_chapters
