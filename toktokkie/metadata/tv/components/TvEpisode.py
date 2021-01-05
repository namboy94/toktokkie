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

from typing import Dict, Any
from toktokkie.exceptions import InvalidMetadata
from toktokkie.metadata.base.components.Component import Component


class TvEpisode(Component):
    """
    Class that models a TV Episode
    """

    def __init__(self, season: int, episode: int):
        """
        Initializes the TvEpisode object
        :param season: The season of the episode
        :param episode: The episode number
        """
        self.season = season
        self.episode = episode

    @property
    def json(self) -> Dict[str, Any]:
        """
        :return: The object represented as JSON data
        """
        return {"season": self.season, "episode": self.episode}

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "TvEpisode":
        """
        Generates a TvEpisode object from json data
        :param json_data: The JSON data
        :return: The generated TvEpisode object
        :raises InvalidMetadataException: If the provided JSON is invalid
        """
        try:
            return cls(json_data["season"], json_data["episode"])
        except KeyError as e:
            raise InvalidMetadata(f"Attribute missing: {e}")
