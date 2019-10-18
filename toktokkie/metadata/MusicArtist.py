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

            albums.append(album)

        return {"albums": albums}

    @property
    def theme_songs(self) -> List[Dict[str, Any]]:
        """
        :return: All theme songs for this music artist
        """
        return list(filter(
            lambda x: x["album_type"] == "theme_song",
            self.json["albums"]
        ))

    def _validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        for album, album_path in listdir(self.directory_path, no_files=True):
            self._assert_true(album in self.json["albums"],
                              "Missing album in metadata: {}".format(album))
