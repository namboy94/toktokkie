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

from abc import ABC
from typing import List, Dict, Optional
from toktokkie.neometadata.enums import IdType
from toktokkie.exceptions import InvalidMetadata
from toktokkie.neometadata.base.MetadataBase import MetadataBase
from toktokkie.neometadata.tv.components.TvSeason import TvSeason
from toktokkie.neometadata.tv.components.TvEpisode import TvEpisode
from toktokkie.neometadata.tv.components.TvEpisodeRange import TvEpisodeRange


class TvExtras(MetadataBase, ABC):
    """
    Extra properties and methods specific to tv series
    """

    @property
    def seasons(self) -> List[TvSeason]:
        """
        :return: A list of TV seasons
        """
        seasons_list = list(map(
            lambda x: TvSeason.from_json(self.directory_path, self.ids, x),
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
                    episode_range = TvEpisodeRange.from_json(exclude)
                    episodes = episode_range.episodes
                except InvalidMetadata:
                    episodes = [TvEpisode.from_json(exclude)]

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
        return self.json.get("season_start_overrides", {})

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
                episode_range = TvEpisodeRange.from_json(multi_episode)

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
            episode: int,
            end_episode: Optional[int] = None
    ):
        """
        Adds an excluded episode
        :param id_type: The ID type
        :param season: The season of the excluded episode
        :param episode: The excluded episode number
        :param end_episode: Optional end episode for multi-episode excludes
        :return: None
        """
        if "excludes" not in self.json:
            self.json["excludes"] = {}
        if id_type.value not in self.json["excludes"]:
            self.json["excludes"][id_type.value] = []

        exclude = {"season": season}
        if end_episode is None:
            exclude.update({"episode": episode})
        else:
            exclude.update({
                "start_episode": episode, "end_episode": end_episode
            })

        self.json["excludes"][id_type.value].append(exclude)

    def add_season_start_override(
            self, id_type: IdType, season: int, episode: int
    ):
        """
        Adds a new season start override
        :param id_type: The ID type
        :param season: The season
        :param episode: The episode
        :return: None
        """
        if "season_start_overrides" not in self.json:
            self.json["season_start_overrides"] = {}
        if id_type not in self.json["season_start_overrides"]:
            self.json["season_start_overrides"][id_type] = {}

        self.json["season_start_overrides"][id_type][season] = episode
