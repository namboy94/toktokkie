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

from copy import deepcopy
from typing import Dict, Any, List
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.components.enums import MediaType, valid_id_types
from puffotter.os import listdir
from puffotter.prompt import prompt


class MusicArtist(Metadata):
    """
    Metadata class that model a music artist
    """

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        return MediaType.MUSIC_ARTIST

    @classmethod
    def _prompt(cls, directory_path: str, json_data: Dict[str, Any]) \
            -> Dict[str, Any]:
        """
        Prompts the user for metadata-type-specific information
        Should be extended by child classes
        :param directory_path: The path to the directory for which to generate
                               the metadata
        :param json_data: Previously generated JSON data
        :return: The generated metadata JSON data
        """
        album_types = {"album", "theme_song", "single"}
        albums = []

        for album, album_path in listdir(directory_path, no_files=True):

            album_data = {
                "name": album,
                "album_type": prompt(
                    "Album Type ({})".format(album), choices=album_types
                ),
                "genre": prompt("Genre"),
                "year": prompt("Year", _type=int)
            }

            if album_data["album_type"] == "theme_song":
                valid = list(set(
                    valid_id_types[MediaType.TV_SERIES]
                    + valid_id_types[MediaType.VISUAL_NOVEL]
                ))
                album_data["series_ids"] = \
                    cls.prompt_for_ids(album_path, valid_options=valid)
                album_data["theme_type"] = prompt(
                    "Theme Type",
                    choices={"OP", "ED", "Insert", "Special", "Other"}
                )

            albums.append(album_data)

        return {"albums": albums}

    def add_album(self, album_data: Dict[str, Any]):
        """
        Adds an album to the metadata
        :param album_data: The album metadata to add
        :return: None
        """
        if album_data["album_type"] == "theme_song":
            ids = album_data["series_ids"]
            album_data["series_ids"] = {}
            for key, value in ids.items():
                album_data["series_ids"][key.value] = value
        self.logger.debug("Adding album metadata: {}".format(album_data))
        self.json["albums"].append(album_data)

    @property
    def all_albums(self) -> List[Dict[str, Any]]:
        """
        :return: All album metadata
        """
        return self.albums + self.singles + self.theme_songs

    @property
    def albums(self) -> List[Dict[str, Any]]:
        """
        :return: All 'album' album metadata
        """
        return list(filter(
                lambda x: x["album_type"] == "album",
                self.json["albums"]
        ))

    @property
    def singles(self) -> List[Dict[str, Any]]:
        """
        :return: All 'single' album metadata
        """
        return list(filter(
            lambda x: x["album_type"] == "single",
            self.json["albums"]
        ))

    @property
    def theme_songs(self) -> List[Dict[str, Any]]:
        """
        :return: All theme songs for this music artist
        """
        valid = list(set(
            valid_id_types[MediaType.TV_SERIES]
            + valid_id_types[MediaType.VISUAL_NOVEL]
        ))

        themes = []
        for theme in list(filter(
            lambda x: x["album_type"] == "theme_song",
            deepcopy(self.json["albums"])
        )):
            ids = {}
            for id_type in valid:
                ids[id_type] = theme["series_ids"].get(id_type.value, [])
            theme["series_ids"] = ids
            themes.append(theme)
        return themes

    def _validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        album_names = [x["name"] for x in self.json["albums"]]

        for album, album_path in listdir(self.directory_path, no_files=True):
            self._assert_true(album in album_names,
                              "Missing album in metadata: {}".format(album))
