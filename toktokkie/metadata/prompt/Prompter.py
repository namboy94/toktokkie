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
import logging
from typing import Dict, Any, List, Tuple
from puffotter.os import listdir
from puffotter.prompt import prompt, yn_prompt, prompt_comma_list
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.ids.IdFetcher import IdFetcher
from toktokkie.metadata.ids.mappings import valid_id_types, int_id_types, \
    id_prompt_order, required_id_types, theme_song_ids
from toktokkie.metadata.MediaType import MediaType


# noinspection PyMethodMayBeStatic
class Prompter:
    """
    Cass that handles prompting for metadata information
    """

    logger = logging.getLogger(__name__)
    """
    Logger for this class
    """

    def __init__(self, directory: str, media_type: MediaType):
        """
        Initializes the Prompter object
        :param directory: The directory for which to prompt for metadata for
        :param media_type: The media type of the directory's content
        """
        self.directory = directory
        self.media_type = media_type
        self.name = os.path.basename(self.directory)
        self.id_fetcher = IdFetcher(self.name, self.media_type)

    def prompt(self) -> Dict[str, Any]:
        """
        Prompts the user for metadata information
        :return: The metadata JSON that resulted from the user's input
        """
        print("Generating metadata for {}:".format(self.name))
        valid_ids = valid_id_types[self.media_type]
        required_ids = required_id_types[self.media_type]

        data = {
            "type": self.media_type.value,
            "tags": prompt_comma_list("Tags"),
            "ids": self.__prompt_ids(valid_ids, required_ids, {})
        }

        if self.media_type == MediaType.BOOK:
            data.update(self.__prompt_book(data))
        elif self.media_type == MediaType.BOOK_SERIES:
            data.update(self.__prompt_book_series(data))
        elif self.media_type == MediaType.MANGA:
            data.update(self.__prompt_manga(data))
        elif self.media_type == MediaType.MOVIE:
            data.update(self.__prompt_movie(data))
        elif self.media_type == MediaType.MUSIC_ARTIST:
            data.update(self.__prompt_music_artist(data))
        elif self.media_type == MediaType.TV_SERIES:
            data.update(self.__prompt_tv_series(data))
        elif self.media_type == MediaType.VISUAL_NOVEL:
            data.update(self.__prompt_visual_novel(data))
        else:
            self.logger.error("No prompt functionality for media type {}"
                              .format(self.media_type.name))

        return data

    def __prompt_ids(
            self,
            valid_ids: List[IdType],
            required_ids: List[IdType],
            defaults: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Prompts the user for any valid IDs the metadata may contain
        :param valid_ids: IDs that are valid for the prompt
        :param required_ids: IDs that are required to be provided
        :param defaults: Any potential default values for the IDs
        :return: The IDs in a dictionary mapping the ID names to their IDs
        """
        ids = {}  # type: Dict[str, List[str]]
        for id_type in id_prompt_order:
            if id_type not in valid_ids:
                continue
            else:
                self.__load_default_ids(valid_ids, defaults)

                default = defaults.get(id_type.value)
                is_int = id_type in int_id_types

                min_count = 0
                if id_type in required_ids:
                    min_count = 1

                ids[id_type.value] = prompt_comma_list(
                    "{} IDs".format(id_type.value),
                    min_count=min_count,
                    default=default,
                    primitive_type=int if is_int else lambda x: str(x)
                )

                non_default = ids[id_type.value] == default

                # Update anilist IDs if myanimelist IDs were updated
                if id_type == IdType.MYANIMELIST and non_default:
                    if IdType.ANILIST.value in defaults:
                        defaults.pop(IdType.ANILIST.value)

        return ids

    def __prompt_component_ids(
            self,
            valid_ids: List[IdType],
            previous_ids: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Prompts for IDs for a component (for example, a season of a tv series)
        Strips away any IDs that are the same as the root metadata ids
        :param valid_ids: ID Types that are valid for the kind of metadata
        :param previous_ids: The IDs previously aquired
        :return: The prompted IDs, mapped to id type strings
        """

        defaults = previous_ids.copy()
        ids = self.__prompt_ids(valid_ids, [], defaults)

        # Strip unnecessary IDs
        for key, value in ids.items():
            if previous_ids.get(key) == value:
                ids.pop(key)

        return ids

    def __load_default_ids(
            self,
            valid_ids: List[IdType],
            defaults: Dict[str, List[str]]
    ):
        """
        Tries to load any missing default IDs using the name of the directory
        and/or other default IDs
        :param valid_ids: List of valid ID types
        :param defaults: The current default IDs
        :return: None (Works in-place)
        """
        _defaults = {}
        for id_type_str, ids in defaults.items():
            _defaults[IdType(id_type_str)] = ids

        for id_type in valid_ids:
            if id_type in defaults:
                continue
            else:
                ids = self.id_fetcher.fetch_ids(id_type, _defaults)
                if ids is not None:
                    defaults[id_type.value] = ids

    # noinspection PyUnusedLocal
    def __prompt_book(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes additional prompts for book metadata
        :param data: The data from the generic prompt
        :return: The additionally generated data
        """
        return {}

    def __prompt_book_series(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes additional prompts for book series metadata
        :param data: The data from the generic prompt
        :return: The additionally generated data
        """
        volumes = {}  # type: Dict[str, Any]
        valid_ids = valid_id_types[self.media_type]

        for i, (volume_name, _) in enumerate(
                listdir(self.directory, no_dirs=True)
        ):
            print("Volume {} ({}):".format(i + 1, volume_name))
            ids = self.__prompt_component_ids(valid_ids, data["ids"])
            volumes[str(i + 1)] = {
                "ids": ids
            }

        return {
            "volumes": volumes
        }

    # noinspection PyUnusedLocal
    def __prompt_manga(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes additional prompts for manga metadata
        :param data: The data from the generic prompt
        :return: The additionally generated data
        """
        special_path = os.path.join(self.directory, "Special")
        special_chapters = []  # type: List[str]

        if os.path.isdir(special_path):
            print("Please enter identifiers for special chapters:")

            special_files = listdir(special_path, no_dirs=True)
            for name, _ in special_files:
                print(name)

            special_chapters = prompt_comma_list(
                "Special Chapters", min_count=len(special_files)
            )

        return {
            "special_chapters": special_chapters
        }

    # noinspection PyUnusedLocal
    def __prompt_movie(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes additional prompts for movie metadata
        :param data: The data from the generic prompt
        :return: The additionally generated data
        """
        return {}

    # noinspection PyUnusedLocal
    def __prompt_music_artist(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes additional prompts for music artist metadata
        :param data: The data from the generic prompt
        :return: The additionally generated data
        """
        albums = []
        theme_songs = []

        for album, album_path in listdir(self.directory, no_files=True):
            print(album)

            album_data = {
                "name": album,
                "genre": prompt("Genre"),
                "year": prompt("Year", _type=int)
            }
            albums.append(album_data)

            if yn_prompt("Is this a theme song?"):
                theme_data = {
                    "name": album,
                    "theme_type": prompt(
                        "Theme Type",
                        choices={"OP", "ED", "Insert", "Special", "Other"}
                    ),
                    "series_data": self.__prompt_ids(theme_song_ids, [], {})
                }
                theme_songs.append(theme_data)

        return {"albums": albums, "theme_songs": theme_songs}

    def __prompt_tv_series(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes additional prompts for tv series metadata
        :param data: The data from the generic prompt
        :return: The additionally generated data
        """
        seasons = []
        valid_ids = valid_id_types[self.media_type]

        # Make sure that regular Seasons are prompted first and in order
        season_folders = []  # type: List[Tuple[str, str]]
        special_folders = []  # type: List[Tuple[str, str]]
        unsorted_folders = listdir(self.directory, no_files=True)

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
            ids = self.__prompt_component_ids(valid_ids, data["ids"])

            seasons.append({
                "ids": ids,
                "name": season_name
            })

        return {
            "seasons": seasons
        }

    # noinspection PyUnusedLocal
    def __prompt_visual_novel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes additional prompts for visual novel metadata
        :param data: The data from the generic prompt
        :return: The additionally generated data
        """
        return {}
