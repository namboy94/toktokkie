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
from typing import List, Dict
from toktokkie.metadata.new.Metadata import Metadata
from toktokkie.metadata.new.wrappers import json_parameter
from toktokkie.metadata.new.components.TvSeason import TvSeason
from toktokkie.metadata.new.id_types import TvIdType
from toktokkie.metadata.new.components.Episode import TvEpisode
from toktokkie.metadata.new.components.EpisodeRange import TvEpisodeRange
from toktokkie.metadata.new.prompt.CommaList import CommaList
from toktokkie.exceptions import InvalidMetadataException


class TvSeries(Metadata):
    """
    Metadata class that model a TV Series
    """

    @classmethod
    def prompt(cls, directory_path: str) -> Metadata:
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """

        seasons = []
        previous = None
        for season_dir in os.listdir(directory_path):

            if season_dir.startswith(".") or not os.path.isdir(season_dir):
                continue

            print(season_dir)

            ids = {}
            for id_type in TvIdType:

                if previous is None:
                    if id_type != TvIdType.TVDB:
                        default = None
                    else:
                        default = CommaList("")
                else:
                    default = CommaList(",".join(previous.ids[id_type]))

                ids[id_type.value] = cls.input(
                    "{} IDs".format(id_type.value),
                    default,
                    CommaList
                ).value

            previous = TvSeason(directory_path, {"ids": ids})
            seasons.append(previous)

        return cls(directory_path, {"seasons": seasons})

    @property
    @json_parameter
    def seasons(self) -> List[TvSeason]:
        """
        :return: A list of TV seasons
        """
        return list(map(
            lambda x: TvSeason(self.directory_path, x),
            self.json["seasons"]
        ))

    @property
    @json_parameter
    def excludes(self) -> Dict[TvIdType, List[TvEpisode]]:
        """
        :return: A dictionary mapping episodes to exclude in checks or renaming
                 operations to id types
        """
        generated = {}

        for _id_type in self.json.get("excludes", {}):

            id_type = TvIdType(_id_type)
            generated[id_type] = []

            for exclude in self.json["excludes"][_id_type]:

                try:
                    episode_range = TvEpisodeRange(exclude)
                    generated[id_type] += episode_range.episodes
                except InvalidMetadataException:
                    generated[id_type].append(TvEpisode(exclude))

        return generated

    @property
    @json_parameter
    def season_start_overrides(self) -> Dict[TvIdType, TvEpisode]:
        """
        :return: A dictionary mapping episodes that override a season starting
                 point to ID types
        """

        generated = {}

        for id_type, episode_data in \
                self.json.get("season_start_overrides", {}):
            generated[TvIdType(id_type)] = TvEpisode(episode_data)

        return generated

    @property
    @json_parameter
    def multi_episodes(self) -> Dict[TvIdType, List[TvEpisodeRange]]:
        """
        :return: A dictionary mapping lists of multi-episodes to id types
        """
        generated = {}

        for _id_type in self.json.get("multi_episodes", {}):

            id_type = TvIdType(_id_type)
            generated[id_type] = []

            for multi_episode in self.json["multi_episodes"][_id_type]:
                generated[id_type].append(TvEpisodeRange(multi_episode))

        return generated

    def validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        super().validate_json()
        self._assert_true("seasons" in self.json)
        self._assert_true(len(self.seasons) == len(self.json["seasons"]))
        self._assert_true(len(self.excludes) == len(self.json.get("excludes")))
        self._assert_true(
            len(self.season_start_overrides) ==
            len(self.json.get("season_start_overrides"))
        )
        self._assert_true(
            len(self.multi_episodes) ==
            len(self.json.get("multi_episodes"))
        )
