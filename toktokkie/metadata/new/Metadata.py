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
import json
from enum import Enum
from functools import wraps
from typing import List, Dict, Any, Callable
from toktokkie.exceptions import InvalidMetadataException, \
    MissingMetadataException


class Metadata:
    """
    Class that acts as the base class for all possible metadata types
    """

    def __str__(self) -> str:
        """
        :return: A string representation of the metadata
        """
        return str(self.json)

    def __repr__(self) -> str:
        """
        :return: A string that could re-generate the metadata object
        """
        return "{}({})".format(self.__class__.__name__, self.directory_path)

    @property
    def name(self) -> str:
        """
        :return: The name of the media
        """
        return os.path.basename(self.directory_path)

    @property
    def tags(self) -> List[str]:
        """
        :return: A list of tags
        """
        return self.json.get("tags", [])

    @tags.setter
    def tags(self, tags: List[str]):
        """
        Setter method for the tags property
        :param tags: The tags to set
        :return: None
        """
        self.json["tags"] = tags

    def __init__(self, directory_path: str, json_data: Dict[str, Any]):
        """
        Inititalizes the metadata object using JSON data
        :param directory_path: The directory of the media for which to
                               generate the metadata
        :param json_data: The JSON data to generate the metadata
        :raises InvalidMetadataException: if the metadata could not be
                                          parsed correctly
        """
        self.directory_path = directory_path
        self.metadata_file = os.path.join(directory_path, ".meta/info.json")
        self.json = json_data
        self.validate_json()

    def validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        for tag in self.tags:
            self._assert_true(type(tag) == str)

    @staticmethod
    def _assert_true(condition: bool):
        """
        Makes sure a statement is true by raising an exception if it's not
        :param condition: The condition to check
        :raises InvalidMetadataException: If the condition was False
        :return: Nine
        """
        if not condition:
            raise InvalidMetadataException()

    @staticmethod
    def _json_parameter(func: Callable) -> Callable:
        """
        Implements additional error-catching for JSON parameters
        :param func: The function to wrap
        :return: The wrapped function
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (KeyError, ValueError):
                raise InvalidMetadataException()

        return wrapper

    def write(self):
        """
        Writes the metadata to the metadata file
        :return: None
        """
        with open(self.metadata_file, "w") as f:
            f.write(json.dumps(
                self.json,
                sort_keys=True,
                indent=4,
                separators=(",", ": ")
            ))

    @classmethod
    def from_directory(cls, directory_path: str):
        """
        Generates metadata for an existing media directory
        :param directory_path: The path to the media directory
        :raises InvalidMetadataException: if the metadata could not be
                                          parsed correctly
        :raises MissingMetadataException: if no metadata file was found
        :return: The generated metadata object
        """
        metadata_file = os.path.join(directory_path, ".meta/info.json")

        if not os.path.isfile(metadata_file):
            raise MissingMetadataException()

        try:
            with open(metadata_file, "r") as info_json:
                data = json.load(info_json)
                return cls(directory_path, data)

        except json.JSONDecodeError:
            raise InvalidMetadataException()

    @classmethod
    def prompt(cls, diretory_path: str):
        """
        Generates a new Metadata object using prompts for a directory
        :return: The generated metadata object
        """
        raise NotImplementedError()






class GenericEpisode:

    def __init__(self, json_data: Dict[Any]):
        self.json = json_data

class GenericEpisodeRange:

    def __init__(self, json_data: Dict[Any]):
        self.json = json_data

class IdType(Enum):
    TVDB = "tvdb",
    MYANIMELIST = "myanimelist",


class TvSeason:

    def __init__(self, json_data: Dict[Any]):
        self.json = json_data


class TvSeries(Metadata):

    @property
    @Metadata._json_parameter
    def seasons(self) -> List[TvSeason]:
        return list(map(lambda x: TvSeason(x), self.json["seasons"]))

    @property
    @Metadata._json_parameter
    def excludes(self) \
            -> Dict[IdType, List[GenericEpisode or GenericEpisodeRange]]:

        generated = {}

        for _id_type in self.json.get("excludes", []):

            id_type = IdType(_id_type)
            generated[id_type] = []

            for exclude in self.json["excludes"][_id_type]:
                if "start_episode" in exclude:
                    generated[id_type].append(GenericEpisodeRange(exclude))
                else:
                    generated[id_type].append(GenericEpisode(exclude))

        return generated

    @property
    @Metadata._json_parameter
    def season_start_overrides(self):
        return

    @property
    @Metadata._json_parameter
    def multi_episodes(self):
        return

    def validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        super().validate_json()
        self._assert_true("seasons" in self.json)
        self._assert_true(len(self.seasons) == len(self.json["seasons"]))
        self._assert_true(len(self.excludes) == len(self.json.get("excludes")))


