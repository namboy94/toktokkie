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
from puffotter.os import listdir
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.components.TvSeason import TvSeason
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.MediaType import MediaType
from toktokkie.metadata.components.TvEpisode import TvEpisode
from toktokkie.metadata.components.TvEpisodeRange import TvEpisodeRange
from toktokkie.exceptions import InvalidMetadata


class TvSeries(Metadata):
    """
    Metadata class that model a TV Series
    """

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        return MediaType.TV_SERIES

    @property
    def tvdb_id(self) -> str:
        """
        :return: The TVDB ID of the TV Series
        """
        return self.ids[IdType.TVDB][0]

    @property
    def seasons(self) -> List[TvSeason]:
        """
        :return: A list of TV seasons
        """
        seasons_list = list(map(
            lambda x: TvSeason(self, x),
            self.json["seasons"]
        ))
        seasons_list.sort(
            key=lambda season: season.name.replace("Season ", "")
        )
        return seasons_list

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
    def excludes(self) -> Dict[IdType, Dict[int, List[int]]]:
        """
        Generates data for episodes to be excluded during renaming etc.
        :return A dictionary mapping episode anithemes to seasons and id types
                Form: {idtype: {season: [ep1, ep2]}}
        """
        generated = {}  # type: Dict[IdType, Dict[int, List[int]]]

        for _id_type in self.json.get("excludes", {}):

            id_type = IdType(_id_type)
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
    def season_start_overrides(self) -> Dict[IdType, Dict[int, int]]:
        """
        :return: A dictionary mapping episodes that override a season starting
                 point to ID types
                 Form: {idtype: {season: episode}}
        """
        generated = {}  # type: Dict[IdType, Dict[int, int]]

        for _id_type, overrides in \
                self.json.get("season_start_overrides", {}).items():

            id_type = IdType(_id_type)
            if id_type not in generated:
                generated[id_type] = {}

            for override in overrides:

                episode = TvEpisode(override)
                generated[id_type][episode.season] = episode.episode

        return generated

    @property
    def multi_episodes(self) -> Dict[IdType, Dict[int, Dict[int, int]]]:
        """
        :return: A dictionary mapping lists of multi-episodes to id types
                 Form: {idtype: {season: {start: end}}}
        """
        generated = {}  # type: Dict[IdType, Dict[int, Dict[int, int]]]

        for _id_type in self.json.get("multi_episodes", {}):

            id_type = IdType(_id_type)
            generated[id_type] = {}

            for multi_episode in self.json["multi_episodes"][_id_type]:
                episode_range = TvEpisodeRange(multi_episode)

                season_number = episode_range.season
                start = episode_range.start_episode
                end = episode_range.end_episode

                if episode_range.season not in generated[id_type]:
                    generated[id_type][season_number] = {}

                generated[id_type][season_number][start] = end

        return generated

    def add_multi_episode(
            self,
            id_type: IdType,
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
            id_type: IdType,
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

    def validate(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        super().validate()
        foldercount = len(listdir(self.directory_path, no_files=True))

        if len(self.seasons) < foldercount:
            raise InvalidMetadata("Missing seasons in metadata")
        elif len(self.seasons) > foldercount:
            raise InvalidMetadata("Missing season directories")

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
        content_info = {}  # type: Dict[str, Dict[int, List[str]]]

        for season_name in os.listdir(self.directory_path):

            season_path = os.path.join(self.directory_path, season_name)
            if season_name.startswith(".") or os.path.isfile(season_path):
                continue

            try:
                season_metadata = self.get_season(season_name)
            except KeyError:
                self.logger.warning(
                    "No Metadata found for {}".format(season_name)
                )
                continue
            tvdb_id = season_metadata.tvdb_id

            if tvdb_id not in content_info:
                content_info[tvdb_id] = {}

            season_number = season_metadata.season_number
            if season_metadata.is_spinoff():
                season_number = 1

            if season_number not in content_info[tvdb_id]:
                content_info[tvdb_id][season_number] = []

            for episode in os.listdir(season_metadata.path):
                episode_path = os.path.join(season_metadata.path, episode)

                if not os.path.isfile(episode_path) or episode.startswith("."):
                    continue

                content_info[tvdb_id][season_number].append(
                    episode_path
                )

        # Sort the episode lists
        for tvdb_id in content_info:
            for season in content_info[tvdb_id]:
                content_info[tvdb_id][season].sort(
                    key=lambda x: os.path.basename(x)
                )

        return content_info
