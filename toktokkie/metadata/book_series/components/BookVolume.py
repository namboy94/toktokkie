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
from typing import Dict, List, Any
from toktokkie.exceptions import InvalidMetadata
from toktokkie.enums import IdType
from toktokkie.metadata.base.components.Component import Component
from toktokkie.utils.ids import stringify_ids, objectify_ids,\
    minimize_ids, fill_ids


class BookVolume(Component):
    """
    Class that models a Volume in a Book Series
    """

    def __init__(
            self,
            volume_number: int,
            path: str,
            parent_ids: Dict[IdType, List[str]],
            ids: Dict[IdType, List[str]]
    ):
        """
        Initializes the Book Volume
        :param volume_number: The volume number
        :param path: The path to the volume file
        :param parent_ids: The IDs of the parent BookSeries object
        :param ids: The specific IDs for this book volume
        """
        self.number = volume_number
        self.path = path
        self.ids = fill_ids(ids, [], parent_ids)
        self.parent_ids = parent_ids

    @property
    def name(self) -> str:
        """
        The name of the volume
        :return: None
        """
        return os.path.basename(self.path).rsplit(".", 1)[0]

    @property
    def json(self) -> Dict[str, Any]:
        """
        :return: A JSON-compatible dictionary representing this object
        """
        return {
            "ids": stringify_ids(minimize_ids(self.ids, self.parent_ids))
        }

    @classmethod
    def from_json(
            cls,
            volume_number: int,
            path: str,
            parent_ids: Dict[IdType, List[str]],
            json_data: Dict[str, Dict[str, List[str]]]
    ) -> "BookVolume":
        """
        Generates a BookVolume object based on json data
        :param volume_number: The volume number
        :param path: The path to the volume file
        :param parent_ids: The IDs of the parent metadata
        :param json_data: The JSON data
        :return: None
        :raises InvalidMetadataException: If the provided JSON is invalid
        """
        try:
            return cls(
                volume_number,
                path,
                parent_ids,
                objectify_ids(json_data["ids"])
            )
        except KeyError as e:
            raise InvalidMetadata(f"Attribute missing: {e}")
