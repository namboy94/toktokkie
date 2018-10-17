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
from toktokkie.metadata.new.id_types import TvIdType
from toktokkie.exceptions import InvalidMetadataException


class TvSeason:
    """
    Class that models a TV Season
    """

    def __init__(self, parent_dir: str, json_data: Dict[str, Any]):
        """
        Initializes the TV Season object using JSON data
        :param parent_dir: The path to the parent directory
        :param json_data: THe JSON data used to generate the TV Season object
        :raises InvalidMetadataException: If any errors were encoutered
                                          while generating the object
        """
        self.json = json_data

        try:
            self.path = os.path.join(parent_dir, self.json["name"])
            if not os.path.isdir(self.path):
                raise InvalidMetadataException()
            # noinspection PyStatementEffect
            self.ids

        except (KeyError, ValueError):
            raise InvalidMetadataException()

    @property
    def name(self) -> str:
        """
        :return: The name of the season
        """
        return self.json["name"]

    @property
    def ids(self) -> Dict[TvIdType, List[str]]:
        """
        :return: A dictionary containing lists of IDs mapped to ID types
        """
        generated = {}
        for id_type, ids in self.json["ids"]:
            generated[TvIdType(id_type)] = list(map(lambda x: str(x), ids))
        return generated
