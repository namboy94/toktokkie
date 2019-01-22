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

import os
import tvdb_api
from datetime import datetime
from toktokkie.check.Checker import Checker
from toktokkie.renaming.Renamer import Renamer
from toktokkie.renaming.RenameOperation import RenameOperation
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

    def _find_file(self, filename: str) -> bool:
        metadata = self.metadata  # type: TvSeries
        exists = False
        for season in metadata.seasons:
            path = os.path.join(season.path, filename)
            exists = exists or os.path.isfile(path)
        return exists

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
            series_data = tvdb_api.Tvdb()[int(tvdb_id)]
        except tvdb_api.tvdb_shownotfound:
            self.error("Show not found on TVDB")
            return

        excluded = metadata.excludes.get(TvIdType.TVDB, {})
        multis = metadata.multi_episodes.get(TvIdType.TVDB, {})
        start_overrides = \
            metadata.season_start_overrides.get(TvIdType.TVDB, {})

        ignores = {}

        for season, episodes in excluded.items():
            ignores[season] = ignores.get(season, []) + episodes
        for season, _multis in multis.items():
            for start, end in _multis.items():
                ignore = list(range(start + 1, end + 1))
                ignores[season] = ignores.get(season, []) + ignore
        for season, start in start_overrides.items():
            ignore = list(range(1, start))
            ignores[season] = ignores.get(season, []) + ignore

        media_content = metadata.get_season_episode_map()

        for season_number, season_data in series_data.items():

            episode_count = len(season_data.keys())

            for episode_number, episode_data in season_data.items():

                airdate = episode_data["firstAired"]
                now = datetime.now().strftime("%Y-%m-%d")

                # Skip unaired episodes
                if airdate > now or not airdate:
                    episode_count -= 1
                    continue

                if episode_number not in ignores:

                    end = None
                    if episode_number in multis.get(season_number, {}):
                        end = multis[season_number][episode_number]

                    exists = False
                    for ext in ["mp4", "mkv", "avi", "m4v"]:

                        episode_name = episode_data["episodename"]
                        if end is not None:
                            episode_name = Renamer.load_tvdb_episode_name(
                                tvdb_id, season_number, episode_number, end
                            )

                        episode_name = Renamer.generate_tv_episode_filename(
                            "a.{}".format(ext),
                            metadata.name,
                            season_number,
                            episode_number,
                            episode_name
                        )
                        episode_name = RenameOperation.sanitize(
                            metadata.directory_path, episode_name
                        )

                        exists = exists or self._find_file(episode_name)

                    if not exists:
                        self.error(
                            "Episode S{}E{} does not exist "
                            "or is incorrectly named".format(
                                str(season_number).zfill(2),
                                str(episode_number).zfill(2)
                                )
                            )
                        # TODO Correctly handle multi episodes

            season_content = media_content.get(season_number, {})
            season_content_count = len(season_content.get("episodes", []))
            season_ignores = ignores.get(season_number, [])
            season_ignores_count = len(season_ignores)

            total_present = season_content_count + season_ignores_count

            if episode_count != total_present:
                self.error("Mismatch in season {}; Should:{}; Is:{}".format(
                    season_number, episode_count, total_present
                ))

# TODO Figure out problem with Seisen Cerberus
