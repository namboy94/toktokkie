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
from abc import ABC
from collections import OrderedDict
from typing import Optional, Any, Dict, List
from toktokkie.enums import MediaType, IdType
from toktokkie.metadata.base.IdHelper import IdHelper


class MetadataBase(IdHelper, ABC):
    """
    Base class for all metadata classes. Specifies most of the
    methods required by Metadata classes.
    """

    logger = logging.getLogger(__name__)
    """
    Logger for the metadata class
    """

    directory_path: str
    """
    The path to the directory this metadata describes
    """

    json: Dict[str, Any]

    @property
    def metadata_file(self) -> str:
        """
        :return: The path to the metadata file
        """
        return os.path.join(self.directory_path, ".meta/info.json")

    @property
    def icon_directory(self) -> str:
        """
        :return: The path to the the icon directory
        """
        return os.path.join(self.directory_path, ".meta/icons")

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
        return self.fill_ids(
            self.objectify_ids(self.json["ids"]),
            self.valid_id_types()
        )

    @ids.setter
    def ids(self, ids: Dict[IdType, List[str]]):
        """
        Setter method for the IDs of the metadata object.
        Previous IDs will be overwritten!
        :param ids: The IDs to set
        :return: None
        """
        self.json["ids"] = self.stringify_ids(self.minimize_ids(ids))

    @property
    def urls(self) -> Dict[IdType, List[str]]:
        """
        Generates URLs for the stored ID types of this metadata object
        URLS are unique and won't show up more than once
        :return: The URLs mapped to their respective id types
        """
        urls = self.generate_urls()
        for id_type in urls.keys():
            urls[id_type] = list(OrderedDict.fromkeys(urls[id_type]))
        return urls

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def valid_id_types(cls) -> List[IdType]:
        """
        :return: Valid ID types for the metadata
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def required_id_types(cls) -> List[IdType]:
        """
        :return: Required ID types for the metadata
        """
        return []  # pragma: no cover

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

    def generate_urls(self) -> Dict[IdType, List[str]]:
        """
        Generates URLs for the stored ID types of this metadata object
        :return: The URLs mapped to their respective id types
        """
        ids = self.ids
        urls: Dict[IdType, List[str]] = {x: [] for x in IdType}

        for id_type, values in ids.items():
            urls[id_type] = [
                self.generate_url_for_id(id_type, self.media_type(), x)
                for x in values
            ]

        return urls
