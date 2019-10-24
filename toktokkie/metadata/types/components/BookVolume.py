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

from typing import Dict, List, Any
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.ids.functions import stringify_ids, objectify_ids,\
    minimize_ids, fill_ids


class BookVolume:
    """
    Class that models a Volume in a Book Series
    """

    def __init__(
            self,
            volume_number: int,
            volume_name: str,
            path: str,
            parent_ids: Dict[IdType, List[str]],
            json_data: Dict[str, Dict[str, List[str]]]
    ):
        """
        Initializes the Book Volume
        :param volume_number: The volume number
        :param volume_name: THe volume name
        :param path: The path to the volume file
        :param parent_ids: The IDs of the parent BookSeries object
        :param json_data: The JSON data for the book volume containing the
                          IDs for this specific volume
        """
        self.volume_number = volume_number
        self.volume_name = volume_name
        self.path = path
        self.ids = fill_ids(objectify_ids(json_data["ids"]), [], parent_ids)
        self.parent_ids = parent_ids

    @property
    def json(self) -> Dict[str, Any]:
        """
        :return: A JSON-compatible dictionary representing this object
        """
        return {
            "ids": stringify_ids(minimize_ids(self.ids, self.parent_ids))
        }
