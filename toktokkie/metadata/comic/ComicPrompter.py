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
from typing import Dict, Any, List
from puffotter.os import listdir, makedirs
from puffotter.prompt import prompt_comma_list
from toktokkie.metadata.base.Prompter import Prompter
from toktokkie.metadata.comic.ComicExtras import ComicExtras


class ComicPrompter(Prompter, ComicExtras, ABC):
    """
    Implements the Prompter functionality for comic metadata
    """

    @classmethod
    def prompt(cls, directory_path: str) -> Dict[str, Any]:
        """
        Generates new Metadata JSON using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata JSON
        """
        base = super().prompt(directory_path)

        main_path = os.path.join(directory_path, "Main")
        makedirs(main_path)
        special_path = os.path.join(directory_path, "Special")
        special_chapters: List[str] = []

        if os.path.isdir(special_path):
            print("Please enter identifiers for special chapters:")

            special_files = listdir(special_path, no_dirs=True)
            for name, _ in special_files:
                print(name)

            special_chapters = prompt_comma_list(
                "Special Chapters", min_count=len(special_files)
            )

        base.update({
            "special_chapters": special_chapters
        })
        return base
