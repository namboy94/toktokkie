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
from toktokkie.metadata.ids.mappings import valid_id_types
from toktokkie.metadata.MediaType import MediaType


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
