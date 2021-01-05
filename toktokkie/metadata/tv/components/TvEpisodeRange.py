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

from typing import Dict, Any, List
from toktokkie.metadata.tv.components.TvEpisode import TvEpisode
from toktokkie.metadata.base.components.JsonComponent import JsonComponent
from toktokkie.exceptions import InvalidMetadata


class TvEpisodeRange(JsonComponent):
    """
    Class that models a TV Episode Range
    """

    def __init__(self, season: int, start_episode: int, end_episode: int):
        """
        Initializes the TvEpisodeRange object
        :param season: The season
        :param start_episode: The first episode in the range
        :param end_episode: The last episode in the range
        """
        self.season = season
        self.start_episode = start_episode
        self.end_episode = end_episode

    @property
    def episodes(self) -> List[TvEpisode]:
        """
        :return: A list of episodes included in this episode range
        """
        episodes = []
        min_episode = min(self.start_episode, self.end_episode)
        max_episode = max(self.start_episode, self.end_episode)

        for episode in range(min_episode, max_episode + 1):
            episodes.append(TvEpisode(self.season, episode))

        return episodes

    @property
    def json(self) -> Dict[str, Any]:
        """
        :return: A JSON-compatible dictionary representing the object
        """
        return {
            "season": self.season,
            "start_episode": self.start_episode,
            "end_episode": self.end_episode
        }

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "TvEpisodeRange":
        """
        Generates a TvEpisodeRange object based on json data
        :param json_data: The JSON data
        :return: The generated TvEpisodeRange object
        :raises InvalidMetadataException: If the provided JSON is invalid
        """
        try:
            return cls(
                json_data["season"],
                json_data["start_episode"],
                json_data["end_episode"]
            )
        except (KeyError, TypeError) as e:
            raise InvalidMetadata(f"Attribute Missing/Invalid: {e}")
