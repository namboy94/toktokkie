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
import tvdb_api
from typing import List, Dict
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.helper.wrappers import json_parameter
from toktokkie.metadata.components.TvSeason import TvSeason
from toktokkie.metadata.components.enums import TvIdType, MediaType
from toktokkie.metadata.components.TvEpisode import TvEpisode
from toktokkie.metadata.components.TvEpisodeRange import TvEpisodeRange
from toktokkie.exceptions import InvalidMetadata


class TvSeries(Metadata):
    """
    Metadata class that model a TV Series
    """

    @classmethod
    def id_type(cls) -> type(TvIdType):
        """
        :return: The ID type used by this metadata object
        """
        return TvIdType

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        return MediaType.TV_SERIES

    @classmethod
    def prompt(cls, directory_path: str) -> Metadata:
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        name = os.path.basename(directory_path)
        print("Generating metadata for {}:".format(name))

        try:
            probable_tvdb_id = str(tvdb_api.Tvdb()[name].data["id"])
            probable_defaults = {TvIdType.TVDB.value: [probable_tvdb_id]}
        except tvdb_api.tvdb_shownotfound:
            probable_defaults = None

        series_ids = cls.prompt_for_ids(defaults=probable_defaults)
        series = cls(directory_path, {
            "seasons": [],
            "ids": series_ids,
            "type": cls.media_type().value
        })

        seasons = []
        for season_name in os.listdir(directory_path):

            season_path = os.path.join(directory_path, season_name)
            if season_name.startswith(".") or not os.path.isdir(season_path):
                continue

            print("\n{}:".format(season_name))
            ids = cls.prompt_for_ids(series_ids)

            # Remove double entries
            for id_type, id_value in series_ids.items():
                if id_value == ids.get(id_type, None):
                    ids.pop(id_type)

            seasons.append(TvSeason(series, {
                "ids": ids,
                "name": season_name
            }))

        series.seasons = seasons
        return series

    @property
    @json_parameter
    def seasons(self) -> List[TvSeason]:
        """
        :return: A list of TV seasons
        """
        return list(map(
            lambda x: TvSeason(self, x),
            self.json["seasons"]
        ))

    @seasons.setter
    def seasons(self, seasons: List[TvSeason]):
        """
        Setter method for the seasons
        :param seasons: The seasons to set
        :return: None
        """
        self.json["seasons"] = []
        for season in seasons:
            self.json["seasons"].append(season.json)

    def get_season(self, season_name: str) -> TvSeason:
        """
        Retrieves a single season for a provided season name
        :param season_name: The name of the season
        :return: The season
        :raises KeyError: If the season could not be found
        """
        for season in self.seasons:
            if season.name == season_name:
                return season
        raise KeyError(season_name)

    @property
    @json_parameter
    def excludes(self) -> Dict[TvIdType, Dict[int, List[int]]]:
        """
        Generates data for episodes to be excluded during renaming etc.
        :return A dictionary mapping episode info to seasons and id types
                Form: {idtype: {season: [ep1, ep2]}}
        """
        generated = {}

        for _id_type in self.json.get("excludes", {}):

            id_type = TvIdType(_id_type)
            generated[id_type] = {}

            for exclude in self.json["excludes"][_id_type]:

                try:
                    episode_range = TvEpisodeRange(exclude)
                    episodes = episode_range.episodes
                except InvalidMetadata:
                    episodes = [TvEpisode(exclude)]

                for episode in episodes:
                    if episode.season not in generated[id_type]:
                        generated[id_type][episode.season] = []
                    generated[id_type][episode.season].append(episode.episode)

        return generated

    @property
    @json_parameter
    def season_start_overrides(self) -> Dict[TvIdType, Dict[int, int]]:
        """
        :return: A dictionary mapping episodes that override a season starting
                 point to ID types
                 Form: {idtype: {season: episode}}
        """
        generated = {}

        for _id_type, overrides in \
                self.json.get("season_start_overrides", {}).items():

            id_type = TvIdType(_id_type)
            if id_type not in generated:
                generated[id_type] = {}

            for override in overrides:

                episode = TvEpisode(override)
                generated[id_type][episode.season] = episode.episode

        return generated

    @property
    @json_parameter
    def multi_episodes(self) -> Dict[TvIdType, Dict[int, Dict[int, int]]]:
        """
        :return: A dictionary mapping lists of multi-episodes to id types
                 Form: {idtype: {season: {start: end}}}
        """
        generated = {}

        for _id_type in self.json.get("multi_episodes", {}):

            id_type = TvIdType(_id_type)
            generated[id_type] = {}

            for multi_episode in self.json["multi_episodes"][_id_type]:
                episode_range = TvEpisodeRange(multi_episode)

                if episode_range.season not in generated[id_type]:
                    generated[id_type] = {}

                generated[id_type][episode_range.season] = {
                    episode_range.start_episode: episode_range.end_episode
                }

        return generated

    def add_multi_episode(
            self,
            id_type: TvIdType,
            season: int,
            start_episode: int,
            end_episode: int
    ):
        """
        Adds a multi-episode
        :param id_type: The ID type
        :param season: The season of the multi episode
        :param start_episode: The start episode
        :param end_episode: The end episode
        :return: None
        """
        if "multi_episodes" not in self.json:
            self.json["multi_episodes"] = {}
        if id_type.value not in self.json["multi_episodes"]:
            self.json["multi_episodes"][id_type.value] = []

        self.json["multi_episodes"][id_type.value].append({
            "season": season,
            "start_episode": start_episode,
            "end_episode": end_episode
        })

    def add_exclude(
            self,
            id_type: TvIdType,
            season: int,
            episode: int
    ):
        """
        Adds an excluded episode
        :param id_type: The ID type
        :param season: The season of the excluded episode
        :param episode: The excluded episode number
        :return: None
        """
        if "excludes" not in self.json:
            self.json["excludes"] = {}
        if id_type.value not in self.json["excludes"]:
            self.json["excludes"][id_type.value] = []

        self.json["excludes"][id_type.value].append({
            "season": season,
            "episode": episode
        })

    def validate_json(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        super().validate_json()
        self._assert_true("seasons" in self.json)
        self._assert_true(len(self.seasons) == len(self.json["seasons"]))
        self._assert_true(
            len(self.excludes) ==
            len(self.json.get("excludes", []))
        )
        self._assert_true(
            len(self.season_start_overrides) ==
            len(self.json.get("season_start_overrides", []))
        )
        self._assert_true(
            len(self.multi_episodes) ==
            len(self.json.get("multi_episodes", []))
        )

    def get_episode_files(self) -> Dict[str, Dict[int, List[str]]]:
        """
        Generates a dictionary categorizing internal episode files for further
        processing.
        A current limitation is, that only a single tvdb ID per season is
        supported. It's currently not planned to lift this limitation,
        as no valid use case for more than one tvdb ID per season has come up.
        The episode lists are sorted by their episode name.
        :return: The generated dictionary. It will have the following form:
                    {tvdb_id: {season_number: [episode_files]}}
        """
        content_info = {}

        for season_name in os.listdir(self.directory_path):

            season_path = os.path.join(self.directory_path, season_name)
            if season_name.startswith(".") or os.path.isfile(season_path):
                continue

            try:
                season_metadata = self.get_season(season_name)
                tvdb_id = season_metadata.ids[TvIdType.TVDB][0]
            except KeyError:
                print("No TVDB ID found for {}".format(season_name))
                continue

            if tvdb_id not in content_info:
                content_info[tvdb_id] = {}

            if season_metadata.season_number not in content_info[tvdb_id]:
                content_info[tvdb_id][season_metadata.season_number] = []

            for episode in os.listdir(season_metadata.path):
                episode_path = os.path.join(season_metadata.path, episode)

                if not os.path.isfile(episode_path) or episode.startswith("."):
                    continue

                content_info[tvdb_id][season_metadata.season_number].append(
                    episode_path
                )

        # Sort the episode lists
        for tvdb_id in content_info:
            for season in content_info[tvdb_id]:
                content_info[tvdb_id][season].sort(
                    key=lambda x: os.path.basename(x)
                )

        for tvdb_id in content_info:
            print(tvdb_id)
            for season in content_info[tvdb_id]:
                print(season)
                for episode in content_info[tvdb_id][season]:
                    print(episode)

        return content_info
