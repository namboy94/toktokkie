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
from typing import Dict
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.verification.Verificator import Verificator
from toktokkie.renaming.helper.resolve import resolve_season, get_episode_files


class TVDBEpisodeCountVerificator(Verificator):
    """
    Verificator that makes sure that all tvdb episodes are properly represented
    by local files.
    """

    applicable_metadata_types = [TvSeries]
    """
    Only applicable to tv series
    """

    def verify(self) -> bool:
        """
        Checks if all tvdb episodes are correctly represented by local files
        :return: True if all episodes are accounted for, False otherwise
        """
        return len(self.__get_incorrect_data()) <= 0

    def fix(self):
        """
        Fixes the issue using prompts
        :return: None
        """
        missing_message = "The amount of episode files conflicts " \
                          "with data from theTVDB\n"
        for season, data in self.__get_incorrect_data().items():
            missing_message += "Season " + str(season) + ": " + \
                               str(data["have"]) + "/" + \
                               str(data["need"]) + "\n"

        self.prompt_until_verified(
            missing_message.strip(),
            "Make sure all episodes are accounted for or excluded or part of "
            "a multi-episode.",
            "Did you correct the errors?",
            "No you didn't."
        )

    def __get_incorrect_data(self) -> Dict[int, Dict[str, int]]:
        """
        Filters out all correct season data from the season completeness data.
        :return: A dictionary mapping incorrect amount of episode files to
                 their repsective seasons
        """
        incorrect = {}
        for season, have_need in self.__get_season_completeness_data().items():
            if have_need["have"] != have_need["need"]:
                incorrect[season] = have_need
        return incorrect

    def __get_season_completeness_data(self) -> Dict[int, Dict[str, int]]:
        """
        Retrieves completeness data for each season
        :return: A dictionary mapping the amount of episodes and the amount
                 of episodes
        """

        tvdb = tvdb_api.Tvdb()
        episode_count = {}  # Keeps track of episodes per season
        file_counts = {}  # Keeps track of actual files per season

        # Only one tvdb id for now
        tvdb_id = self.directory.metadata.seasons.list[0].tvdb_ids.list[0]

        tvdb_data = tvdb[tvdb_id]
        for season_number, season_data in tvdb_data.items():
            file_counts[season_number] = 0
            episode_count[season_number] = 0
            for _ in season_data:
                episode_count[season_number] += 1

        for season in self.directory.metadata.seasons.list:
            season_path = os.path.join(self.directory.path, season.path)
            season_number = resolve_season(season_path)
            file_counts[season_number] += len(get_episode_files(season_path))

        # Consider excluded episodes
        for exclude in self.directory.metadata.tvdb_excludes.list:
            file_counts[exclude.season] += 1

        # Consider multi-episodes
        for multi in self.directory.metadata.tvdb_multi_episodes.list:
            file_counts[multi.start.season] += multi.diff()

        have_need = {}
        for season, count in episode_count.items():
            have_need[season] = {
                "have": file_counts[season],
                "need": count
            }
        return have_need
