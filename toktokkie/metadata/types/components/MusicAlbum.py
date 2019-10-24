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
from typing import Dict, Any, List
from toktokkie.metadata.types.components.Component import Component
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.ids.functions import objectify_ids, stringify_ids, \
    fill_ids, minimize_ids


class MusicAlbum(Component):
    """
    Class that defines attributes of music albums
    """

    def __init__(
            self,
            parent_path: str,
            parent_ids: Dict[IdType, List[str]],
            json_data: Dict[str, Any]
    ):
        """
        Initializes the MusicAlbum object
        :param parent_path: The path to the parent directory
        :param parent_ids: The IDs associated with the parent
        :param json_data: The JSON data of the album
        """
        self.parent_path = parent_path
        self.parent_ids = parent_ids

        self.name = json_data["name"]
        self.genre = json_data["genre"]
        self.year = json_data["year"]
        self.path = os.path.join(parent_path, self.name)

        ids = objectify_ids(json_data.get("ids", {}))
        self.ids = fill_ids(ids, [], parent_ids)

    @property
    def json(self) -> Dict[str, Any]:
        """
        Converts the component into a JSON-compatible dictionary
        :return: The JSON-compatible dictionary
        """
        return {
            "name": self.name,
            "genre": self.genre,
            "year": self.year,
            "ids": stringify_ids(minimize_ids(self.ids, self.parent_ids))
        }
