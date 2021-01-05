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
from abc import ABC
from typing import List, Optional, Dict
from puffotter.os import get_ext, listdir
from tvdb_api import tvdb_episodenotfound, tvdb_seasonnotfound, \
    tvdb_shownotfound
from toktokkie.utils.ImdbCache import ImdbCache
from toktokkie.metadata.base.Renamer import Renamer
from toktokkie.utils.RenameOperation import RenameOperation
from toktokkie.enums import IdType
from toktokkie.metadata.tv.TvExtras import TvExtras


class TvRenamer(Renamer, TvExtras, ABC):
    """
    Class that handles renaming operations for tv series
    """

    @property
    def selected_renaming_id_type(self) -> Optional[IdType]:
        """
        :return: The preferred ID type that's available for renaming
        """
        priority = [IdType.IMDB, IdType.TVDB]
        for id_type in priority:
            if len(self.ids[id_type]) > 0:
                return id_type
        return None

    # noinspection PyMethodMayBeStatic
    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Performs rename operations on the content referenced by
        this metadata object
        :return: The rename operations for this metadata
        """
        operations = []

        id_type = self.selected_renaming_id_type

        if id_type is None:
            excluded, multis, start_overrides = {}, {}, {}
        else:
            excluded = self.excludes.get(id_type, {})
            multis = self.multi_episodes.get(id_type, {})
            start_overrides = self.season_start_overrides.get(id_type, {})

        content_info = self.get_episode_files(id_type)

        for service_id, season_data in content_info.items():

            if id_type is None:
                service_ids = []
            else:
                service_ids = self.ids.get(id_type, [])

            is_spinoff = id_type is not None and service_ids[0] != service_id

            if is_spinoff:
                sample_episode = season_data[list(season_data)[0]][0]
                location = os.path.dirname(sample_episode)
                series_name = os.path.basename(location)
            else:
                series_name = self.name

            for _season_number, episodes in season_data.items():
                season_number = _season_number if not is_spinoff else 1

                season_excluded = excluded.get(season_number, [])
                season_multis = multis.get(season_number, {})
                episode_number = start_overrides.get(season_number, 1)

                for episode_file in episodes:

                    while episode_number in season_excluded:
                        episode_number += 1

                    if episode_number not in season_multis:
                        end = None  # type: Optional[int]
                    else:
                        end = season_multis[episode_number]

                    episode_name = self.load_episode_name(
                        service_id, id_type, season_number, episode_number, end
                    )

                    new_name = self.generate_tv_episode_filename(
                        episode_file,
                        series_name,
                        season_number,
                        episode_number,
                        episode_name,
                        end
                    )

                    if end is not None:
                        episode_number = end

                    operations.append(RenameOperation(episode_file, new_name))
                    episode_number += 1

        return operations

    @staticmethod
    def generate_tv_episode_filename(
            original_file: str,
            series_name: str,
            season_number: int,
            episode_number: int,
            episode_name: str,
            multi_end: Optional[int] = None
    ):
        """
        Generates an episode name for a given episode
        :param original_file: The original file. Used to get the file extension
        :param series_name: The name of the series
        :param season_number: The season number
        :param episode_name: The episode name
        :param episode_number: The episode number
        :param multi_end: Can be provided to create a multi-episode range
        :return: The generated episode name
        """
        ext = get_ext(original_file)
        if ext is not None:
            ext = "." + ext
        else:
            ext = ""

        if multi_end is None:
            return "{} - S{}E{} - {}{}".format(
                series_name,
                str(season_number).zfill(2),
                str(episode_number).zfill(2),
                episode_name,
                ext
            )
        else:
            return "{} - S{}E{}-E{} - {}{}".format(
                series_name,
                str(season_number).zfill(2),
                str(episode_number).zfill(2),
                str(multi_end).zfill(2),
                episode_name,
                ext
            )

    @staticmethod
    def load_episode_name(
            service_id: str,
            id_type: Optional[IdType],
            season_number: int,
            episode_number: int,
            multi_end: Optional[int] = None
    ) -> str:
        """
        Loads an episode name from external sources, if available
        :param service_id: The external service ID for the episode's series
        :param id_type: The external ID type
        :param season_number: The season number
        :param episode_number: The episode number
        :param multi_end: If provided,
                          will generate a name for a range of episodes
        :return: The episode name
        """
        default = "Episode " + str(episode_number)

        if id_type is None or service_id == "0":
            return default

        if multi_end is not None:
            episode_names = []
            for episode in range(episode_number, multi_end + 1):
                episode_names.append(TvRenamer.load_episode_name(
                    service_id,
                    id_type,
                    season_number,
                    episode
                ))
            return " | ".join(episode_names)

        if id_type == IdType.IMDB:
            return ImdbCache.load_episode_name(
                service_id, season_number, episode_number
            )
        elif id_type == IdType.TVDB:  # pragma: no cover
            # Due to tvdb's new paid model, this will no longer be able
            # to be tested in unit tests.
            # IMDB will now be the de-facto default
            try:
                tvdb = tvdb_api.Tvdb()
                info = tvdb[int(service_id)]
                return info[season_number][episode_number]["episodeName"]

            except (tvdb_episodenotfound, tvdb_seasonnotfound,
                    tvdb_shownotfound, ConnectionError, KeyError,
                    AttributeError, ValueError) as e:
                logger = TvRenamer.logger
                # If not found, or other error, just return generic name
                if str(e) == "cache_location":  # pragma: no cover
                    logger.warning("TheTVDB.com is down!")
                elif str(e).startswith("apikey argument is now required"):
                    logger.warning("TheTVDB now requires an API key")
                print(e)
                return default
        else:
            return default

    def get_episode_files(self, id_type: Optional[IdType]) \
            -> Dict[str, Dict[int, List[str]]]:
        """
        Generates a dictionary categorizing internal episode files for further
        processing.
        A current limitation is, that only a single service ID per season is
        supported. It's currently not planned to lift this limitation,
        as no valid use case for more than one ID per season has come up.
        The episode lists are sorted by their episode name.
        :param id_type: The ID type for which to group the episodes
        :return: The generated dictionary. It will have the following form:
                    {service_id: {season_number: [episode_files]}}
        """
        content_info = {}  # type: Dict[str, Dict[int, List[str]]]

        for season_name, season_path in listdir(
                self.directory_path, no_files=True, no_dot=True
        ):
            season_metadata = self.get_season(season_name)
            if id_type is None:
                service_id = "0"
            else:
                service_id = season_metadata.ids.get(id_type, ["0"])[0]

            if service_id not in content_info:
                content_info[service_id] = {}

            season_number = season_metadata.season_number
            if season_metadata.is_spinoff():
                season_number = 1

            if season_number not in content_info[service_id]:
                content_info[service_id][season_number] = []

            for episode, episode_path in listdir(
                    season_metadata.path, no_dirs=True, no_dot=True
            ):
                content_info[service_id][season_number].append(episode_path)

        # Sort the episode lists
        for service_id in content_info:
            for season in content_info[service_id]:
                content_info[service_id][season].sort(
                    key=lambda x: os.path.basename(x)
                )

        return content_info

    def resolve_title_name(self) -> str:
        """
        If possible, will fetch the appropriate name for the
        metadata based on IDs, falling back to the
        directory name if this is not possible or supported.
        """
        return self.load_title_and_year([
            IdType.ANILIST,
            IdType.IMDB
        ])[0]
