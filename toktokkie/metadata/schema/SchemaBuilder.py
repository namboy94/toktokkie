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

import logging
from typing import Dict, Any, List
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.ids.mappings import valid_id_types, required_id_types
from toktokkie.metadata.MediaType import MediaType


# noinspection PyMethodMayBeStatic
class SchemaBuilder:
    """
    Class that defines JSON schemas for the various media types
    """

    logger = logging.getLogger(__name__)
    """
    Logger object for this class
    """

    def __init__(self, media_type: MediaType):
        """
        Initializes the SchemaBuilder using a media type
        :param media_type: The media type for which to generate
                           a JSON schema
        """
        self.media_type = media_type

    def build_schema(self) -> Dict[str, Any]:
        """
        Generates the JSON schema
        :return: The JSON schema
        """
        ids = self.__create_ids_schema(
            valid_id_types[self.media_type],
            required_id_types[self.media_type]
        )
        ids["minProperties"] = 1

        properties = {
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            },
            "ids": ids,
            "type": {
                "type": "string",
                "pattern": "^" + str(self.media_type.value) + "$"
            }
        }
        required = ["type", "ids"]

        if self.media_type == MediaType.BOOK:
            properties.update(self.__create_book_properties())
        elif self.media_type == MediaType.BOOK_SERIES:
            properties.update(self.__create_book_series_properties())
        elif self.media_type == MediaType.MANGA:
            properties.update(self.__create_manga_properties())
        elif self.media_type == MediaType.MOVIE:
            properties.update(self.__create_movie_properties())
        elif self.media_type == MediaType.MUSIC_ARTIST:
            properties.update(self.__create_music_artist_properties())
            required.append("albums")
        elif self.media_type == MediaType.TV_SERIES:
            properties.update(self.__create_tv_series_properties())
            required.append("seasons")
        elif self.media_type == MediaType.VISUAL_NOVEL:
            properties.update(self.__create_visual_novel_properties())
        else:
            self.logger.error("Schema for media type {} not implemented"
                              .format(self.media_type.name))

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    def __create_ids_schema(
            self,
            valid_ids: List[IdType],
            required_ids: List[IdType]
    ) -> Dict[str, Any]:
        """
        Creates an "ids" object that allows any valid ID types
        :param valid_ids: The valid ID types
        :param required_ids: Required ID types
        :return: The "ids" object in JSON schema format
        """
        properties = {}  # type: Dict[str, Any]
        for id_type in valid_ids:
            properties[id_type.value] = {
                "type": "array",
                "items": {"type": "string"}
            }

        return {
            "type": "object",
            "properties": properties,
            "additionalProperties": False,
            "required": [x.value for x in required_ids]
        }

    def __create_book_properties(self) -> Dict[str, Any]:
        """
        Creates additional properties for book metadata
        :return: The additional properties
        """
        return {}

    def __create_book_series_properties(self) -> Dict[str, Any]:
        """
        Creates additional properties for book series metadata
        :return: The additional properties
        """
        ids = self.__create_ids_schema(valid_id_types[self.media_type], [])
        return {
            "volumes": {
                "type": "object",
                "patternProperties": {
                    "^[0-9]+$": {
                        "type": "object",
                        "properties": {
                            "ids": ids
                        }
                    }
                },
                "additionalProperties": False
            }
        }

    def __create_manga_properties(self) -> Dict[str, Any]:
        """
        Creates additional properties for manga metadata
        :return: The additional properties
        """
        return {
            "special_chapters": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }

    def __create_movie_properties(self) -> Dict[str, Any]:
        """
        Creates additional properties for movie metadata
        :return: The additional properties
        """
        return {}

    def __create_music_artist_properties(self) -> Dict[str, Any]:
        """
        Creates additional properties for music artist metadata
        :return: The additional properties
        """
        return {
            "albums": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "genre": {"type": "string"},
                        "year": {"type": "number"},
                        "ids": {}
                    },
                    "required": ["name", "genre", "year"]
                }
            },
            "theme_songs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "series_ids": {},
                        "theme_type": {
                            "type": "string",
                            "pattern": "(op|ed|insert|special|other){1}"
                        }
                    },
                    "required": ["name", "theme_type"]
                }
            }
        }

    def __create_tv_series_properties(self) -> Dict[str, Any]:
        """
        Creates additional properties for tv series metadata
        :return: The additional properties
        """
        valid_ids = valid_id_types[self.media_type]
        ids = self.__create_ids_schema(valid_ids, [])

        excludes = {}
        multi_episodes = {}
        season_start_overrides = {}
        for id_type in valid_ids:
            extra_base = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "season": {"type": "number"},
                        "episode": {"type": "number"}
                    },
                    "required": ["season", "episode"]
                }
            }
            excludes[id_type.value] = extra_base.copy()
            season_start_overrides[id_type.value] = extra_base.copy()

            extra_base = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "season": {"type": "number"},
                        "start_episode": {"type": "number"},
                        "end_episode": {"type": "number"}
                    },
                    "required": ["season", "start_episode", "end_episode"]
                }
            }
            multi_episodes[id_type.value] = extra_base.copy()

        return {
            "seasons": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "ids": ids,
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
                }
            },
            "excludes": {
                "type": "object",
                "additionalProperties": excludes
            },
            "season_start_overrides": {
                "type": "object",
                "additionalProperties": season_start_overrides
            },
            "multi_episodes": {
                "type": "object",
                "additionalProperties": multi_episodes
            }
        }

    def __create_visual_novel_properties(self) -> Dict[str, Any]:
        """
        Creates additional properties for visual novel metadata
        :return: The additional properties
        """
        return {}


if __name__ == "__main__":
    for _media_type in MediaType:
        print(_media_type.value)
        print(SchemaBuilder(_media_type).build_schema())
        print()
