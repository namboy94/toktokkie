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
from typing import Dict, Any, Tuple, List
from puffotter.os import listdir
from toktokkie.neometadata.base.Prompter import Prompter
from toktokkie.neometadata.tv.TvExtras import TvExtras


class TvPrompter(Prompter, TvExtras, ABC):
    """
    Prompter class for tv series
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
        seasons = []

        # Make sure that regular Seasons are prompted first and in order
        season_folders = []  # type: List[Tuple[str, str]]
        special_folders = []  # type: List[Tuple[str, str]]
        unsorted_folders = listdir(directory_path, no_files=True)

        for folder, folder_path in unsorted_folders:
            if folder.startswith("Season "):
                try:
                    int(folder.split("Season ")[1])
                    season_folders.append((folder, folder_path))
                except (ValueError, IndexError):
                    special_folders.append((folder, folder_path))
            else:
                special_folders.append((folder, folder_path))

        season_folders.sort(key=lambda x: int(x[0].split("Season ")[1]))

        for season_name, season_path in season_folders + special_folders:
            print("\n{}:".format(season_name))
            ids = cls._prompt_component_ids(
                cls.valid_id_types(),
                base["ids"],
                cls._create_id_fetcher(directory_path)
            )

            seasons.append({
                "ids": ids,
                "name": season_name
            })

        base.update({
            "seasons": seasons
        })
        return base
