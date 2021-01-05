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
from toktokkie.exceptions import InvalidMetadata
from toktokkie.enums import IdType
from toktokkie.metadata.base.IdHelper import IdHelper
from toktokkie.metadata.base.components.JsonComponent import JsonComponent
from toktokkie.metadata.music.components.MusicAlbum import MusicAlbum


class MusicThemeSong(JsonComponent):
    """
    Class that collects data on music theme songs (like anime openings etc)
    """

    def __init__(
            self,
            album: MusicAlbum,
            name: str,
            theme_type: str,
            series_ids: Dict[IdType, List[str]]
    ):
        """
        Initializes the object
        :param album: The album object related to this theme song
        :param name: The name of the song
        :param theme_type: The type of theme song
        :param series_ids: The IDs of the series this is a theme song for
        """
        self.album = album
        self.name = name
        self._theme_type = theme_type

        if self.name != self.album.name:
            self.logger.warning("Theme song {} does not match album {}"
                                .format(self.name, self.album.name))
        self.series_ids = IdHelper.fill_ids(
            series_ids, IdHelper.theme_song_id_types()
        )

    @property
    def theme_type(self) -> str:
        """
        :return: The theme type
        """
        return self._theme_type.upper()

    @property
    def json(self) -> Dict[str, Any]:
        """
        Converts the component into a JSON-compatible dictionary
        :return: The JSON-compatible dictionary
        """
        return {
            "name": self.name,
            "series_ids": IdHelper.stringify_ids(IdHelper.minimize_ids(
                self.series_ids
            )),
            "theme_type": self.theme_type.lower()
        }

    @classmethod
    def from_json(
            cls,
            album: MusicAlbum,
            json_data: Dict[str, Any]
    ) -> "MusicThemeSong":
        """
        Generates a new MusicThemeSong object based on JSON data
        :param album: The corresponding album object
        :param json_data: The JSON data
        :return: The generated object
        :raises InvalidMetadataException: If the provided JSON is invalid
        """
        try:
            return cls(
                album,
                json_data["name"],
                json_data["theme_type"],
                IdHelper.objectify_ids(json_data["series_ids"])
            )
        except KeyError as e:
            raise InvalidMetadata(f"Attribute missing: {e}")
