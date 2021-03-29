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
from puffotter.prompt import prompt_comma_list, prompt
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

        main_chapters_path = os.path.join(directory_path, "Chapters")
        main_volumes_path = os.path.join(directory_path, "Volumes")
        special_path = os.path.join(directory_path, "Special")
        makedirs(main_chapters_path)
        makedirs(main_volumes_path)
        makedirs(special_path)
        special_chapters: List[str] = []
        chapter_offset = 0

        if len(os.listdir(special_path)) > 0:
            print("Please enter identifiers for special chapters:")

            special_files = listdir(special_path, no_dirs=True)
            for name, _ in special_files:
                print(name)

            special_chapters = prompt_comma_list(
                "Special Chapters", min_count=len(special_files)
            )
        if len(os.listdir(main_chapters_path)) > 0 and len(os.listdir(main_volumes_path)) > 0:
            chapter_offset = prompt(
                "Please enter the chapter offset:", _type=int, default=0
            )

        base.update({
            "special_chapters": special_chapters,
            "chapter_offset": chapter_offset
        })
        return base
