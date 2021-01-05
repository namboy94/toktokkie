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
from puffotter.prompt import prompt, yn_prompt
from toktokkie.metadata.enums import IdType
from toktokkie.metadata.base.Prompter import Prompter
from toktokkie.metadata.music.MusicExtras import MusicExtras
from toktokkie.metadata.utils.ids import theme_song_ids


class MusicPrompter(Prompter, MusicExtras, ABC):
    """
    Implements the Prompter functionality for music metadata
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
        id_fetcher = cls._create_id_fetcher(directory_path)
        albums = []
        theme_songs = []

        for album, album_path in listdir(directory_path, no_files=True):
            print(album)

            valid_album_ids = cls.valid_id_types()
            valid_album_ids.remove(IdType.MUSICBRAINZ_ARTIST)
            valid_album_ids.append(IdType.MUSICBRAINZ_RELEASE)

            album_data = {
                "name": album,
                "genre": prompt("Genre"),
                "year": prompt("Year", _type=int),
                "ids": cls._prompt_component_ids(
                    valid_album_ids, {}, id_fetcher
                )
            }
            albums.append(album_data)

            if yn_prompt("Is this a theme song?"):
                theme_data = {
                    "name": album,
                    "theme_type": prompt(
                        "Theme Type",
                        choices={"OP", "ED", "Insert", "Special", "Other"}
                    ).lower(),
                    "series_ids": cls._prompt_ids(
                        theme_song_ids, [], {}, id_fetcher
                    )
                }
                theme_songs.append(theme_data)

        base.update({"albums": albums, "theme_songs": theme_songs})
        return base
