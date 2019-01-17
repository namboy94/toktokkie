"""
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
"""

import tvdb_api
from toktokkie.check.Checker import Checker
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.metadata.components.enums import TvIdType


class TvSeriesChecker(Checker):
    """
    Class that check TV Series media for consistency
    """

    def check(self):
        """
        Performs sanity checks and prints out anything that's wrong
        :return: None
        """
        super().check()
        self.check_tvdb_completeness()

    def check_tvdb_completeness(self):
        """
        Makes sure that all episodes entered on thetvdb.com are present
        in the directory or otherwise excluded using metadata
        :return: None
        """
        metadata = self.metadata  # type: TvSeries
        tvdb_ids = metadata.ids.get(TvIdType.TVDB, [])
        for season in metadata.seasons:
            tvdb_ids += season.ids.get(TvIdType.TVDB, [])

        try:
            tvdb_id = list(set(tvdb_ids))[0]
        except IndexError:
            self.error("No TVDB ID found")
            return

        try:
            series_data = tvdb_api.Tvdb()[tvdb_id]
        except tvdb_api.tvdb_shownotfound:
            self.error("Show not found on TVDB")
            return

        excluded = metadata.excludes.get(TvIdType.TVDB, {})
        multis = metadata.multi_episodes.get(TvIdType.TVDB, {})
        start_overrides = \
            metadata.season_start_overrides.get(TvIdType.TVDB, {})

        ignores = {}

        for season, episodes in excluded:
            ignores[season] = ignores.get(season, []) + episodes
        for season, _multis in multis:
            for start, end in _multis:
                ignore = list(range(start + 1, end + 1))
                ignores[season] = ignores.get(season, []) + ignore
        for season, start in start_overrides:
            ignore = list(range(1, start))
            ignores[season] = ignores.get(season, []) + ignore

        media_content = metadata.get_season_episode_map()

        for season_number in series_data.keys():
            season_data = series_data[season_number]

            episode_count = len(season_data.keys())

            season_content = media_content.get(season_number, 0)
            season_content_count = len(season_content)
            season_ignores = ignores.get(season_number, 0)
            season_ignores_count = len(season_ignores)

            total_present = season_content_count + season_ignores_count

            if episode_count != total_present:
                self.error("Mismatch in season {}; Should:{}; Is:{}".format(
                    season_number, episode_count, total_present
                ))

            for episode_number in season_data.keys():
                if episode_number not in ignores:
                    pass


