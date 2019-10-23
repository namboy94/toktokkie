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
from typing import List, Dict, Any, Optional
from jsonschema import validate, ValidationError
from toktokkie.exceptions import InvalidMetadata, MissingMetadata
from toktokkie.metadata.schema.SchemaBuilder import SchemaBuilder
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.ids.mappings import valid_id_types
from toktokkie.metadata.MediaType import MediaType
from toktokkie.metadata.prompt.Prompter import Prompter


class Metadata:
    """
    Class that acts as the base class for all possible metadata types
    """

    logger = logging.getLogger(__name__)
    """
    Logger for the metadata class
    """

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        raise NotImplementedError()

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
        self.directory_path = directory_path
        self.metadata_file = os.path.join(directory_path, ".meta/info.json")
        self.icon_directory = os.path.join(directory_path, ".meta/icons")

        if json_data is None:
            with open(self.metadata_file, "r") as info:
                self.json = json.load(info)
        else:
            self.json = json_data

        if not no_validation:
            self.validate()

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

    def validate(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        schema = SchemaBuilder(self.media_type()).build_schema()
        try:
            validate(instance=self.json, schema=schema)
        except ValidationError as e:
            raise InvalidMetadata("Invalid Metadata: {}".format(e))

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

    @classmethod
    def prompt(cls, directory_path: str) -> "Metadata":
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        prompter = Prompter(directory_path, cls.media_type())
        json_data = prompter.prompt()
        return cls(directory_path, json_data)

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
            if id_type in valid_id_types[self.media_type()]:
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
