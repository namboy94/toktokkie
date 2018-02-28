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
from typing import List, Dict
from toktokkie.metadata.Base import Base
from toktokkie.metadata.helper import prompt_user
from toktokkie.metadata.types.TvSeriesSeason import TvSeriesSeason
from toktokkie.metadata.types.MetaType import Str, Int, MetaType, MetaList
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
    def generate_from_prompts(cls, directory: str,
                              extra_data: List[Dict[str, MetaType]] = None):
        """
        Generates a TV Series from user prompts
        :param directory: The directory to generate the metadata for
        :param extra_data: optional parameter that can be used by subclasses
                           to add additional prompts
        :return: The generated metadata object
        """
        tvdb_id = prompt_user("TVDB ID", Int)
        seasons = []

        for season in os.listdir(directory):
            season_dir = os.path.join(directory, season)
            if os.path.isfile(season_dir) or season.startswith(".meta"):
                continue

            if len(seasons) > 0:
                previous = seasons[len(seasons) - 1]
                season_obj = TvSeriesSeason.prompt(season, previous)
            else:
                season_obj = TvSeriesSeason.prompt(season)

            seasons.append(season_obj)

        data = [{
            "tvdb_id": tvdb_id,
            "seasons": MetaList(seasons)
        }]
        if extra_data is not None:
            data += extra_data

        return super().generate_from_prompts(directory, data)

    def to_dict(self) -> dict:
        """
        Turns the metadata into a dictionary
        :return: The dictionary representation of the metadata
        """
        data = super().to_dict()
        data["tvdb_id"] = self.tvdb_id
        data["seasons"] = self.seasons
        return data

    def __init__(self, json_data: dict):
        """
        Initializes the metadata object
        :param json_data: The JSON metadata to use
        """
        super().__init__(json_data)
        try:
            self.tvdb_id = Int.from_json(json_data["tvdb_id"])
            self.seasons = MetaList([])

            for season in json_data["seasons"]:
                self.seasons.append(TvSeriesSeason.from_json(season))

        except KeyError:
            raise InvalidMetadataException()
