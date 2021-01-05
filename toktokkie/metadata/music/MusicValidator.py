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
from toktokkie.exceptions import InvalidMetadata
from toktokkie.enums import IdType
from toktokkie.metadata.base.Validator import Validator
from toktokkie.metadata.music.MusicExtras import MusicExtras


class MusicValidator(Validator, MusicExtras, ABC):
    """
    Implements the Validator functionality for music metadata
    """

    @classmethod
    def build_schema(cls) -> Dict[str, Any]:
        """
        Generates the JSON schema
        :return: The JSON schema
        """
        base = super().build_schema()

        valid_album_ids = cls.valid_id_types()
        valid_album_ids.remove(IdType.MUSICBRAINZ_ARTIST)
        valid_album_ids.append(IdType.MUSICBRAINZ_RELEASE)

        album_ids = cls._create_ids_schema(valid_album_ids)
        series_ids = cls._create_ids_schema(Validator.theme_song_id_types())

        base["properties"].update({
            "albums": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "genre": {"type": "string"},
                        "year": {"type": "number"},
                        "ids": album_ids
                    },
                    "required": ["name", "genre", "year"],
                    "additionalProperties": False
                }
            },
            "theme_songs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "series_ids": series_ids,
                        "theme_type": {
                            "type": "string",
                            "pattern": "(op|ed|insert|special|other){1}"
                        }
                    },
                    "required": ["name", "theme_type"],
                    "additionalProperties": False
                }
            }
        })
        base["required"].append("albums")
        return base

    def validate(self):
        super().validate()
        album_names = [x.name for x in self.albums]
        for theme_song in self.json.get("theme_songs", []):
            name = theme_song["name"]
            if name not in album_names:
                raise InvalidMetadata(f"Missing album data for {name}")
