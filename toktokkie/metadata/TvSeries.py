"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

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
"""

import os
from typing import Dict, List
from toktokkie.metadata.Base import Base
from toktokkie.metadata.types.AgentIdType import AgentIdType
from toktokkie.metadata.types.TvSeriesSeason import TvSeriesSeason
from toktokkie.metadata.types.MetaType import Str, MetaType, MetaList
from toktokkie.metadata.exceptions import InvalidMetadataException


class TvSeries(Base):
    """
    A metadata model for tv series
    """

    type = Str("tv_series")
    """
    The metadata type
    """

    @classmethod
    def generate_dict_from_prompts(cls, directory: str) -> Dict[str, MetaType]:
        """
        Generates a TV Series from user prompts
        :param directory: The directory to generate the metadata for
        :return: The generated metadata dictionary
        """
        data = super().generate_dict_from_prompts(directory)
        seasons = []

        for season in sorted(os.listdir(directory)):
            season_dir = os.path.join(directory, season)
            if os.path.isfile(season_dir) or season.startswith(".meta"):
                continue

            if len(seasons) > 0:
                previous = seasons[len(seasons) - 1]
                season_obj = TvSeriesSeason.prompt(season, previous)
            else:
                season_obj = TvSeriesSeason.prompt(season)

            seasons.append(season_obj)

        data["seasons"] = MetaList(seasons)
        return data

    def to_dict(self) -> Dict[str, MetaType]:
        """
        Turns the metadata into a dictionary
        :return: The dictionary representation of the metadata
        """
        data = super().to_dict()
        data["seasons"] = self.seasons
        return data

    def __init__(self, json_data: dict):
        """
        Initializes the metadata object
        :param json_data: The JSON metadata to use
        """
        super().__init__(json_data)
        try:
            self.seasons = MetaList([])
            self.tvdb_excludes = [{"S": 0, "E": 1}]  # TODO Make user-configurable
            self.tvdb_irregular_season_start_episode = {0: 0}  # TODO Make user-configurable

            for season in json_data["seasons"]:
                self.seasons.append(TvSeriesSeason.from_json(season))

        except KeyError:
            raise InvalidMetadataException()

    def get_agent_excludes(self, id_type: AgentIdType) \
            -> List[Dict[str, int]] or None:
        """
        Retrieves excluded episodes using the provided agent ID type
        :param id_type: The ID type to check for
        :return: The excluded episode list, or None if id type not applicable
        """

        if id_type == AgentIdType.TVDB:
            return self.tvdb_excludes.to_json()
        else:
            return None

    def get_agent_irregular_season_starts(self, id_type: AgentIdType) \
            -> Dict[int, int] or None:
        """
        Retrieves irregular season episode starts for the provided agent type
        :param id_type: The agent ID type
        :return: A dictionary of irregular season starts or None if the id is
                 not applicable
        """

        if id_type == AgentIdType.TVDB:
            return self.tvdb_irregular_season_start_episode.to_json()
        else:
            return None
