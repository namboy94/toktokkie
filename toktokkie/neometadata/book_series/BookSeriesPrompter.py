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

from abc import ABC
from typing import Dict, Any
from puffotter.os import listdir
from toktokkie.exceptions import InvalidDirectoryState
from toktokkie.neometadata.base.Prompter import Prompter
from toktokkie.neometadata.book_series.BookSeriesExtras import BookSeriesExtras


class BookSeriesPrompter(Prompter, BookSeriesExtras, ABC):
    """
    Implements the Prompter functionality for book series metadata
    """

    @classmethod
    def pre_prompt_check(cls, directory_path: str):
        """
        Makes sure that the book series directory has at least one volume
        :param directory_path: The path to the directory to check
        :return: None
        """
        super().pre_prompt_check(directory_path)
        filecount = len(listdir(directory_path, no_dirs=True))
        if filecount == 0:
            raise InvalidDirectoryState("No book files")

    @classmethod
    def prompt(cls, directory_path: str) -> Dict[str, Any]:
        """
        Generates new Metadata JSON using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata JSON
        """
        base = super().prompt(directory_path)
        volumes = {}  # type: Dict[str, Any]
        id_fetcher = cls._create_id_fetcher(directory_path)

        for i, (volume_name, _) in enumerate(
                listdir(directory_path, no_dirs=True)
        ):
            print("Volume {} ({}):".format(i + 1, volume_name))
            ids = cls._prompt_component_ids(
                cls.valid_id_types(), base["ids"], id_fetcher
            )
            volumes[str(i + 1)] = {
                "ids": ids
            }

        base.update({
            "volumes": volumes
        })
        return base
