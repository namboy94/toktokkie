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
from toktokkie.metadata.Base import Base
from toktokkie.metadata.structures import Language
from toktokkie.metadata.structures import TvSeriesSeason
from toktokkie.metadata.exceptions import InvalidMetadataException
from toktokkie.metadata.types import CommaList, IntCommaList, \
    ResolutionCommaList, LanguageCommaList


class TvSeries(Base):
    """
    A metadata model for tv series
    """

    type = "tv_series"
    """
    The metadata type
    """

    @classmethod
    def generate_from_prompts(cls, directory: str, extra_data: dict = None):
        """
        Generates a TV Series from user prompts
        :param directory: The directory to generate the metadata for
        :param extra_data: optional parameter that can be used by subclasses
                           to add additional prompts
        :return: The generated metadata object
        """
        data = {
            "tvdb_id": cls.prompt_user("TVDB ID", int),
            "seasons": []
        }

        for season in os.listdir(directory):
            season_dir = os.path.join(directory, season)
            if os.path.isfile(season_dir) or season.startswith(".meta"):
                continue

            print("Season \"" + season + "\":")

            season_data = {
                "name": cls.prompt_user("Name", str, season),
                "tvdb_ids": cls.prompt_user("TVDB IDs", IntCommaList).list,
                "audios": cls.prompt_user(
                    "Audio Languages", LanguageCommaList,
                    LanguageCommaList("eng")
                ).list,
                "subtitles": cls.prompt_user(
                    "Subtitle Languages", LanguageCommaList,
                    LanguageCommaList()
                ).list,
                "resolutions": cls.prompt_user(
                    "Resolutions", ResolutionCommaList
                ).list
            }

            data["seasons"].append(TvSeriesSeason(season, season_data))

        data = [data]
        if extra_data is not None:
            for extra in extra_data:
                data.append(extra)

        return super().generate_from_prompts(directory, data)

    def to_dict(self) -> dict:
        """
        Turns the metadata into a dictionary
        :return: The dictionary representation of the metadata
        """
        data = super().to_dict()
        data["tvdb_id"] = self.tvdb_id
        data["seasons"] = list(map(lambda x: x.to_json(), self.seasons))
        return data

    def __init__(self, json_data: dict):
        """
        Initializes the metadata object
        :param json_data: The JSON metadata to use
        """
        super().__init__(json_data)
        try:
            self.tvdb_id = json_data["tvdb_id"]
            self.seasons = []

            for season_name, season_data in json_data["seasons"].items():
                self.seasons.append(TvSeriesSeason(season_name, season_data))

        except KeyError:
            raise InvalidMetadataException()
