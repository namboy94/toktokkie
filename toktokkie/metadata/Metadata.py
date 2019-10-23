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
import logging
import tvdb_api
import musicbrainzngs
from typing import List, Dict, Any, Optional
from jsonschema import validate, ValidationError
from toktokkie import version
from toktokkie.exceptions import InvalidMetadata, MissingMetadata
from toktokkie.metadata.schema.SchemaBuilder import SchemaBuilder
from toktokkie.metadata.components.enums import MediaType, IdType, \
    valid_id_types, required_id_types
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.MediaType import MediaType as \
    AnimeListMediaType
from puffotter.prompt import prompt_comma_list


class Metadata:
    """
    Class that acts as the base class for all possible metadata types
    """

    def __init__(
            self,
            directory_path: str,
            json_data: Optional[Dict[str, Any]] = None,
            no_validation: bool = False
    ):
        """
        Inititalizes the metadata object using JSON data
        :param directory_path: The directory of the media for which to
                               generate the metadata
        :param json_data: Optional metadata JSON.
                          Will be used instead of info.json metadata
                          if provided
        :param no_validation: Skips JSON validation if True
        :raises InvalidMetadataException: if the metadata could not be
                                          parsed correctly
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.directory_path = directory_path
        self.metadata_file = os.path.join(directory_path, ".meta/info.json")
        self.icon_directory = os.path.join(directory_path, ".meta/icons")

        if json_data is None:
            with open(self.metadata_file, "r") as info:
                self.json = json.load(info)
        else:
            self.json = json_data

        if not no_validation:
            self.validate_json()

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

    def __eq__(self, other: object) -> bool:
        """
        Checks equality with another object
        :param other: The other object
        :return: True if equal, False otherwise
        """
        if not isinstance(other, type(self)):
            return False
        else:
            return self.json == other.json

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
        directory = self.directory_path
        if directory.endswith("/"):
            directory = directory.rsplit("/", 1)[0]
        new_path = os.path.join(os.path.dirname(directory), name)
        os.rename(directory, new_path)
        self.directory_path = new_path

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

    @property
    def ids(self) -> Dict[IdType, List[str]]:
        """
        :return: A dictionary containing lists of IDs mapped to ID types
        """
        generated = {}
        for id_type, _id in self.json["ids"].items():

            if isinstance(_id, list):
                generated[IdType(id_type)] = _id
            else:
                generated[IdType(id_type)] = [_id]

        for id_type in IdType:
            if id_type in self.valid_id_types():
                if id_type not in generated:
                    generated[id_type] = []

        return generated

    @ids.setter
    def ids(self, ids: Dict[IdType, List[str]]):
        """
        Setter method for the IDs of the metadata object.
        Previous IDs will be overwritten!
        :param ids: The IDs to set
        :return: None
        """
        self.json["ids"] = {}
        for id_type, values in ids.items():
            self.json["ids"][id_type.value] = values

    def set_ids(self, id_type: IdType, ids: List[str]):
        """
        Sets IDs for one ID type to the metadata
        :param id_type: The id type
        :param ids: The IDs to set
        :return: None
        """
        metadata_ids = self.ids
        metadata_ids[id_type] = ids
        self.ids = metadata_ids

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
        return valid_id_types[cls.media_type()]

    def validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        schema = SchemaBuilder(self.media_type()).build_schema()
        try:
            validate(instance=self.json, schema=schema)
        except ValidationError as e:
            raise InvalidMetadata(str(e))

        try:
            self._assert_true(
                os.path.isdir(self.directory_path),
                "Directory path does not exist"
            )
            for tag in self.tags:
                self._assert_true(type(tag) == str, "Tag isn't a string")
            self._assert_true("ids" in self.json, "No IDs in metadata")

            active_ids = self.ids
            for id_type in IdType:
                ids = active_ids.get(id_type, [])
                if len(ids) == 0 and id_type in active_ids:
                    active_ids.pop(id_type)

            for _, ids in self.ids.items():
                for _id in ids:
                    self._assert_true(type(_id) == str, "ID is not string")

            for id_type in self.required_ids():
                self._assert_true(
                    id_type.value in self.json["ids"],
                    "Required ID {} missing".format(id_type.value)
                )
            for id_type in self.ids:
                self._assert_true(
                    id_type in self.valid_id_types(),
                    "Invalid ID type {}".format(id_type.value)
                )

            self._assert_true(
                len(active_ids) == len(self.json["ids"]),
                "ID amount invalid"
            )
            self._assert_true(len(active_ids) > 0, "No IDs")
            self._assert_true(
                self.media_type().value == self.json["type"],
                "Invalid Media Type"
            )
            self._validate_json()
        except (ValueError, TypeError, KeyError):
            raise InvalidMetadata("Unknown Error in Metadata")

    def _validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        Should be implemented by child classes
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        raise NotImplementedError()

    def write(self):
        """
        Writes the metadata to the metadata file
        :return: None
        """
        self.logger.debug("Writing Metadata: {}".format(self.json))

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
    def prompt(cls, directory_path: str) -> "Metadata":
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        print("Generating metadata for {}:"
              .format(os.path.basename(directory_path)))

        json_data = {
            "type": cls.media_type().value,
            "tags": prompt_comma_list("Tags: "),
        }

        defaults = {}  # type: Dict[str, List[str]]
        if IdType.TVDB in cls.valid_id_types():
            try:
                name = os.path.basename(os.path.abspath(directory_path))
                probable_tvdb_id = str(tvdb_api.Tvdb()[name].data["id"])
                defaults[IdType.TVDB.value] = [probable_tvdb_id]
            except (tvdb_api.tvdb_shownotfound, TypeError):
                pass

        json_data["ids"] = \
            cls.prompt_for_ids(directory_path, defaults=defaults)

        json_data.update(cls._prompt(directory_path, json_data))
        return cls(directory_path, json_data)

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
    def prompt_for_ids(
            cls,
            directory: str,
            defaults: Optional[Dict[str, List[str]]] = None,
            valid_options: Optional[List[IdType]] = None
    ) -> Dict[str, List[str]]:
        """
        Prompts the user for IDs
        :param directory: The directory for which to prompt the IDs
        :param defaults: The default values to use, mapped to id type names
        :param valid_options: Overrides valid ID type options
        :return: The generated IDs. At least one ID will be included
        """
        ids = {}  # type: Dict[str, List[str]]
        mal_updated = False
        id_order = [
            IdType.TVDB,
            IdType.IMDB,
            IdType.ISBN,
            IdType.VNDB,
            IdType.MUSICBRAINZ,
            IdType.MYANIMELIST,
            IdType.ANILIST,
            IdType.KITSU,
            IdType.MANGADEX
        ]
        if valid_options is None:
            valid = cls.valid_id_types()
            required = cls.required_ids()
        else:
            valid = valid_options
            required = []

        while len(ids) < 1:

            for id_type in id_order:
                if id_type not in valid:
                    continue

                default = None  # type: Optional[List[str]]
                if defaults is not None:
                    default = defaults.get(id_type.value, [])
                elif id_type not in required:
                    default = []

                # Load anilist ID from myanimelist ID
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
                        default = anilist_ids

                min_count = 1 if id_type in required else 0

                if id_type == IdType.MUSICBRAINZ:
                    musicbrainzngs.set_useragent(
                        "toktokkie media manager",
                        version,
                        "https://gitlab.namibsun.net/namibsun/python/toktokie"
                    )
                    artist_guess = musicbrainzngs.search_artists(
                        os.path.basename(directory)
                    )
                    if artist_guess["artist-count"] > 0:
                        default = [artist_guess["artist-list"][0]["id"]]

                if id_type in [
                    IdType.ISBN,
                    IdType.IMDB,
                    IdType.VNDB,
                    IdType.MUSICBRAINZ
                ]:
                    prompted = prompt_comma_list(
                        "{} IDs: ".format(id_type.value),
                        min_count=min_count,
                        default=default,
                        primitive_type=lambda x: str(x)
                    )
                else:
                    prompted = prompt_comma_list(
                        "{} IDs: ".format(id_type.value),
                        min_count=min_count,
                        default=default,
                        primitive_type=int
                    )

                prompted = list(map(lambda x: str(x), prompted))

                if len(prompted) > 0:
                    ids[id_type.value] = prompted

                    # Check if myanimelist ID was updated
                    if id_type.value == IdType.MYANIMELIST.value:
                        if default is not None:
                            mal_updated = prompted != default

            if len(ids) < 1:
                print("Please provide at least one ID")

        return ids

    @classmethod
    def required_ids(cls) -> List[IdType]:
        """
        :return: A list of required IDs for the metadata type
        """
        return required_id_types[cls.media_type()]

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

    @staticmethod
    def _assert_true(condition: bool, fail_message: str = "Unknown Error"):
        """
        Makes sure a statement is true by raising an exception if it's not
        :param condition: The condition to check
        :param fail_message: Message displayed when False, should be indicative
                             of the error
        :raises InvalidMetadataException: If the condition was False
        :return: Nine
        """
        if not condition:
            raise InvalidMetadata(fail_message)
