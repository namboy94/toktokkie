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
from typing import Dict, List, Any, Union
from puffotter.os import listdir
from toktokkie.exceptions import InvalidMetadata
from toktokkie.metadata.base.components.Component import Component
from toktokkie.enums import IdType
from toktokkie.utils.ids import objectify_ids, stringify_ids,\
    fill_ids, minimize_ids


class TvSeason(Component):
    """
    Class that models a season of a TV Series
    """

    def __init__(
            self,
            parent_path: str,
            parent_ids: Dict[IdType, List[str]],
            ids: Dict[IdType, List[str]],
            name: str
    ):
        """
        Initializes the TvSeason object
        :param parent_path: The path to the parent metadata directory
        :param parent_ids: The IDs of the parent metadata
        :param ids: The specific IDs for this season
        :param name: The name of the season
        """
        self.parent_path = parent_path
        self.parent_ids = parent_ids

        self.name = name
        self.path = os.path.join(parent_path, self.name)

        self.ids = fill_ids(ids, [], parent_ids)

    @property
    def json(self) -> Dict[str, Any]:
        """
        :return: A JSON-compatible dictionary representing this object
        """
        return {
            "name": self.name,
            "ids": stringify_ids(minimize_ids(self.ids, self.parent_ids))
        }

    @classmethod
    def from_json(
            cls,
            parent_path: str,
            parent_ids: Dict[IdType, List[str]],
            json_data: Dict[str, Union[str, Dict[str, List[str]]]]
    ):
        """
        Generates a TvSeason object based on JSON data
        :param parent_path: The path to the parent metadata directory
        :param parent_ids: The IDs of the parent metadata
        :param json_data: The JSON data
        :return: The generated TvSeason object
        :raises InvalidMetadataException: If the provided JSON is invalid
        """
        try:
            return cls(
                parent_path,
                parent_ids,
                objectify_ids(json_data["ids"]),
                json_data["name"]
            )
        except KeyError as e:
            raise InvalidMetadata(f"Attribute missing: {e}")

    @property
    def season_number(self) -> int:
        """
        :return: The season number of the season
        """
        if self.name.lower().startswith("season "):
            return int(self.name.lower().split("season")[1])
        else:
            return 0

    def is_spinoff(self) -> bool:
        """
        :return: Whether or not this season is a spinoff
        """
        return self.parent_ids.get(IdType.TVDB) != self.ids.get(IdType.TVDB)

    @property
    def episode_names(self) -> List[str]:
        """
        :return: A sorted list of episode names
        """
        return [
            x[0].rsplit(".", 1)[0] for x in listdir(self.path, no_dirs=True)
        ]
