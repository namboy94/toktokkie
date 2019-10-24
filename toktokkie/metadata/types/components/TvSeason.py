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
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.ids.functions import minimize_ids, fill_ids, \
    objectify_ids, stringify_ids


class TvSeason:
    """
    Class that models a season of a TV Series
    """

    def __init__(
            self,
            parent_path: str,
            parent_ids: Dict[IdType, List[str]],
            json_data: Dict[str, Union[Dict[str, List[str]], str]]
    ):
        self.parent_path = parent_path
        self.parent_ids = parent_ids

        self.name = json_data["name"]
        self.path = os.path.join(parent_path, self.name)
        self.ids = fill_ids(objectify_ids(json_data["ids"]), [], parent_ids)

    @property
    def json(self) -> Dict[str, Any]:
        """
        :return: A JSON-compatible dictionary representing this object
        """
        return {
            "name": self.name,
            "ids": stringify_ids(minimize_ids(self.ids, self.parent_ids))
        }

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
