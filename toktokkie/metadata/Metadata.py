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
from typing import List, Dict, Any, Optional
from toktokkie.metadata.helper.wrappers import json_parameter
from toktokkie.metadata.prompt.PromptType import PromptType
from toktokkie.metadata.prompt.CommaList import CommaList
from toktokkie.exceptions import InvalidMetadata, \
    MissingMetadata
from toktokkie.metadata.components.enums import MediaType, IdType
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.MediaType import MediaType as \
    AnimeListMediaType


class Metadata:
    """
    Class that acts as the base class for all possible metadata types
    """

    def __str__(self) -> str:
        """
        :return: A string representation of the metadata
        """
        json_data = json.dumps(
            self.json,
            sort_keys=True,
            indent=4,
            separators=(",", ": ")
        )
        return "Name: {}\nMedia Type: {}\nInfo:\n{}".format(
            self.name,
            self.media_type().name,
            json_data
        )

    def __repr__(self) -> str:
        """
        :return: A string that could re-generate the metadata object
        """
        return "{}({}, {})".format(
            self.__class__.__name__,
            self.directory_path,
            str(self.json)
        )

    @property
    def name(self) -> str:
        """
        :return: The name of the media
        """
        return os.path.basename(os.path.abspath(self.directory_path))

    @name.setter
    def name(self, name: str):
        """
        Renames the media directory
        :param name: The new name of the media directory
        :return: None
        """
        new_path = os.path.join(os.path.dirname(self.directory_path), name)
        os.rename(self.directory_path, new_path)
        self.directory_path = new_path

    @property
    @json_parameter
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

    @property
    @json_parameter
    def ids(self) -> Dict[Enum, List[str]]:
        """
        :return: A dictionary containing lists of IDs mapped to ID types
        """
        generated = {}
        for id_type, _id in self.json["ids"].items():

            if isinstance(_id, list):
                generated[IdType(id_type)] = _id
            else:
                generated[IdType(id_type)] = [_id]

        return generated

    @ids.setter
    def ids(self, ids: Dict[Enum, List[str]]):
        """
        Setter method for the IDs of the metadata object.
        Previous IDs will be overwritten!
        :param ids: The IDs to set
        :return: None
        """
        self.json["ids"] = {}
        for id_type, values in ids.items():
            self.json["ids"][id_type.value] = values

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        raise NotImplementedError()

    @classmethod
    def valid_id_types(cls) -> List[IdType]:
        """
        :return: The types of IDs that are valid for this metadata type
        """
        return {
            MediaType.MANGA: [
                IdType.MANGADEX,
                IdType.ANILIST,
                IdType.MYANIMELIST,
                IdType.KITSU
            ],
            MediaType.TV: [
                IdType.ANILIST,
                IdType.KITSU,
                IdType.MYANIMELIST,
                IdType.TVDB
            ],
            MediaType.MOVIE: [
                IdType.ANILIST,
                IdType.KITSU,
                IdType.MYANIMELIST,
                IdType.TVDB
            ],
            MediaType.BOOK: [
                IdType.ISBN,
                IdType.ANILIST,
                IdType.KITSU,
                IdType.MYANIMELIST
            ],
            MediaType.BOOK_SERIES: [
                IdType.ISBN,
                IdType.ANILIST,
                IdType.KITSU,
                IdType.MYANIMELIST
            ],
            MediaType.VISUAL_NOVEL: [
                IdType.VNDB
            ]
        }[cls.media_type()]

    def __init__(
            self,
            directory_path: str,
            json_data: Optional[Dict[str, Any]] = None
    ):
        """
        Inititalizes the metadata object using JSON data
        :param directory_path: The directory of the media for which to
                               generate the metadata
        :param json_data: Optional metadata JSON.
                          Will be used instead of info.json metadata
                          if provided
        :raises InvalidMetadataException: if the metadata could not be
                                          parsed correctly
        """
        self.directory_path = directory_path
        self.metadata_file = os.path.join(directory_path, ".meta/info.json")
        self.icon_directory = os.path.join(directory_path, ".meta/icons")

        if json_data is None:
            with open(self.metadata_file, "r") as info:
                self.json = json.load(info)
        else:
            self.json = json_data

        self.validate_json()

    def validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        self._assert_true(os.path.isdir(self.directory_path))
        for tag in self.tags:
            self._assert_true(type(tag) == str)
        self._assert_true("ids" in self.json)
        self._assert_true(len(self.ids) == len(self.json["ids"]))
        self._assert_true(len(self.ids) > 0)
        self._assert_true(self.media_type().value == self.json["type"])

    def write(self):
        """
        Writes the metadata to the metadata file
        :return: None
        """
        if not os.path.isdir(os.path.dirname(self.metadata_file)):
            os.makedirs(os.path.dirname(self.metadata_file))

        self.json["type"] = self.media_type().value

        with open(self.metadata_file, "w") as f:
            f.write(json.dumps(
                self.json,
                sort_keys=True,
                indent=4,
                separators=(",", ": ")
            ))

    @classmethod
    def prompt(cls, directory_path: str):
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        raise NotImplementedError()

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
            raise MissingMetadata()

        try:
            with open(metadata_file, "r") as info_json:
                data = json.load(info_json)
                return cls(directory_path, data)

        except json.JSONDecodeError:
            raise InvalidMetadata()

    @classmethod
    def input(
            cls,
            prompt_text: str,
            default: Optional[PromptType],
            _type: type(PromptType),
            required: bool = False
    ) -> Any:
        """
        Creates a user prompt that supports default options and automatic
        type conversions.
        :param prompt_text: The text to prompt the user
        :param default: The default value to use
        :param _type: The type of the prompted value
        :param required: Whether or not a response is required
        :return: The user's response
        """
        if default is not None:
            prompt_text += " {}".format(str(default))
        prompt_text += ":"

        response = input(prompt_text).strip()
        while response == "" and default is None:
            response = input(prompt_text).strip()

        if response == "" and default is not None:
            return default
        elif response == "" and required:
            return cls.input(prompt_text, default, _type, required)
        else:
            try:
                return _type(response)
            except (TypeError, ValueError):
                return cls.input(prompt_text, default, _type, required)

    @classmethod
    def prompt_for_ids(
            cls,
            defaults: Optional[Dict[str, List[str]]] = None,
            required: Optional[List[Enum]] = None
    ) -> Dict[str, List[str]]:
        """
        Prompts the user for IDs
        :param defaults: The default values to use, mapped to id type names
        :param required: A list of required ID types
        :return: The generated IDs. At least one ID will be included
        """
        required = required if required is not None else []

        ids = {}
        mal_updated = False
        while len(ids) < 1:
            for id_type in cls.valid_id_types():

                if defaults is not None:
                    default = defaults.get(id_type.value, [])
                    default = CommaList(",".join(default))
                else:
                    default = None if id_type in required else CommaList("")

                if IdType.MYANIMELIST.value in ids and mal_updated:
                    if id_type.value == IdType.ANILIST.value:

                        api = AnilistApi()

                        anime_list_media_type = AnimeListMediaType.ANIME
                        if cls.media_type() in [
                            MediaType.MANGA,
                            MediaType.BOOK_SERIES,
                            MediaType.BOOK
                        ]:
                            anime_list_media_type = AnimeListMediaType.MANGA

                        anilist_ids = []
                        for mal_id in ids[IdType.MYANIMELIST.value]:
                            anilist_id = api.get_anilist_id_from_mal_id(
                                anime_list_media_type,
                                int(mal_id)
                            )
                            anilist_ids.append(str(anilist_id))
                        default = CommaList(",".join(anilist_ids))

                prompted = cls.input(
                    "{} IDs".format(id_type.value),
                    default,
                    CommaList,
                    required=(id_type in required)
                ).value

                prompted = list(filter(lambda x: x != "", prompted))

                if len(prompted) > 0:
                    ids[id_type.value] = prompted

                    # Check if myanimelist ID was updated
                    if id_type.value == IdType.MYANIMELIST.value:
                        if default.value is not None:
                            mal_updated = prompted != default.value

            if len(ids) < 1:
                print("Please provide at least one ID")

        return ids

    @staticmethod
    def _assert_true(condition: bool):
        """
        Makes sure a statement is true by raising an exception if it's not
        :param condition: The condition to check
        :raises InvalidMetadataException: If the condition was False
        :return: Nine
        """
        if not condition:
            raise InvalidMetadata()

    def print_folder_icon_source(self):
        """
        Prints a message with a URL for possible folder icons on deviantart
        :return: None
        """
        deviantart = "https://www.deviantart.com"
        url = "{}/popular-all-time/?section=&global=1&q={}".format(
            deviantart,
            "+".join(self.name.split(" ") + ["folder", "icon"])
        )
        print("Search folder icons here:")
        print(url)

    def get_icon_file(self, name: str) -> Optional[str]:
        """
        Retrieves the path to an icon file, if it exists
        :param name: The name of the icon.
        :return: The path to the icon file or None, if the file does not exist
        """
        path = os.path.join(self.icon_directory, "{}.png".format(name))
        if os.path.isfile(path):
            return path
        else:
            return None

    def get_anilist_urls(self) -> List[str]:
        """
        :return: A list of anilist URLs for the series
        """
        media_type = "anime"
        if self.media_type() in [
            MediaType.BOOK, MediaType.BOOK_SERIES, MediaType.MANGA
        ]:
            media_type = "manga"

        urls = []
        for _id in self.ids.get(IdType.ANILIST, []):
            urls.append("https://anilist.co/{}/{}".format(media_type, _id))
        return urls
