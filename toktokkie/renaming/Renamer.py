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
from tvdb_exceptions import tvdb_episodenotfound, tvdb_seasonnotfound, \
    tvdb_shownotfound
from typing import List, Optional
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.metadata.components.enums import MediaType, TvIdType
from toktokkie.renaming.RenameOperation import RenameOperation


class Renamer:
    """
    Class that handles the renaming of a media directory's content
    """

    def __init__(self, metadata: Metadata):
        """
        Initializes the Renamer. ValueErrors will be thrown if an error
        is encountered at any point during the initialization process
        :param metadata: The metadata to use for information
        """
        self.path = metadata.directory_path
        self.metadata = metadata

        if self.metadata.media_type() == MediaType.BOOK:
            self.operations = self._generate_book_operations()
        elif self.metadata.media_type() == MediaType.BOOK_SERIES:
            self.operations = self._generate_book_series_operations()
        elif self.metadata.media_type() == MediaType.MOVIE:
            self.operations = self._generate_movie_operations()
        elif self.metadata.media_type() == MediaType.TV_SERIES:
            self.operations = self._generate_tv_series_operations()
        else:  # pragma: no cover
            self.operations = []  # type: List[RenameOperation]

    def rename(self, noconfirm: bool):
        """
        Renames the contained files according to the naming scheme.
        :param noconfirm: Skips the confirmation phase if True
        :return: None
        """
        if not noconfirm:
            for operation in self.operations:
                print(operation)

            prompt = input("Proceed with renaming? (Y/N)\n")
            while prompt.lower() not in ["y", "n"]:
                prompt = input("(Y/N)")

            if prompt.lower() == "n":
                print("Renaming aborted.")
                return

        for operation in self.operations:
            operation.rename()

    def _get_children(self, no_dirs: bool = False, no_files: bool = False) \
            -> List[str]:
        """
        Retrieves a list of files and/or directories inside the media directory
        that may be valid for renaming
        :param no_dirs: If True, will ignore all directories
        :param no_files: If True, will ignore all files
        :return: A list of child directories/files, excluding hidden or
                 metadata files.
        """
        children = []
        for child in os.listdir(self.path):
            if child.startswith("."):
                continue
            elif os.path.isdir(os.path.join(self.path, child)) and no_dirs:
                continue
            elif os.path.isfile(os.path.join(self.path, child)) and no_files:
                continue
            else:
                children.append(child)

        return sorted(children)

    def _generate_book_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for book media types
        :return: The list of rename operations
        """
        book_file = self._get_children(no_dirs=True)[0]
        dest = "{}.{}".format(self.metadata.name, self._get_ext(book_file))
        return [RenameOperation(
            os.path.join(self.path, book_file),
            os.path.join(self.path, dest)
        )]

    def _generate_book_series_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for book series media types
        :return: The list of rename operations
        """
        operations = []
        children = self._get_children(no_dirs=True)
        fill = len(str(len(children)))

        for i, volume in enumerate(children):
            new_name = "{} - Volume {}".format(
                self.metadata.name,
                str(i + 1).zfill(fill)
            )

            operations.append(RenameOperation(
                os.path.join(self.path, volume),
                os.path.join(self.path, new_name)
            ))

        return operations

    def _generate_movie_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for movie media types
        :return: The list of rename operations
        """
        movie_file = self._get_children(no_dirs=True)[0]
        dest = "{}.{}".format(self.metadata.name, self._get_ext(movie_file))
        return [RenameOperation(
            os.path.join(self.path, movie_file),
            os.path.join(self.path, dest)
        )]

    def _generate_tv_series_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for tv series media types
        TODO Split up in multiple methods.
        :return: The list of rename operations
        """
        operations = []

        tv_series_metadata = self.metadata  # type: TvSeries

        content_info = {}

        excluded = tv_series_metadata.excludes.get(TvIdType.TVDB, {})
        multis = tv_series_metadata.multi_episodes.get(TvIdType.TVDB, {})
        start_overrides = \
            tv_series_metadata.season_start_overrides.get(TvIdType.TVDB, {})

        series_name = tv_series_metadata.name

        for season in self._get_children(no_files=True):

            try:
                season_metadata = tv_series_metadata.get_season(season)
                tvdb_id = season_metadata.ids[TvIdType.TVDB][0]
            except KeyError:
                continue

            if season_metadata.season_number not in content_info:
                content_info[season_metadata.season_number] = {
                    "tvdb_id": tvdb_id,
                    "episodes": []
                }

            for episode in os.listdir(season_metadata.path):
                episode_path = os.path.join(season_metadata.path, episode)

                if not os.path.isfile(episode_path) or episode.startswith("."):
                    continue

                content_info[season_metadata.season_number]["episodes"] \
                    .append(episode_path)

        for season_number, season_data in content_info.items():

            tvdb_id = season_data["tvdb_id"]
            episodes = season_data["episodes"]

            season_excluded = excluded.get(season_number, [])
            season_multis = multis.get(season_number, {})
            episode_number = start_overrides.get(season_number, 1)

            episodes.sort(key=lambda x: os.path.basename(x))

            for episode_file in episodes:

                while episode_number in season_excluded:
                    episode_number += 1

                start = episode_number
                if episode_number in season_multis:
                    end = season_multis[episode_number]
                else:
                    end = None

                ext = self._get_ext(episode_file)

                if end is None:
                    new_name = "{} - S{}E{} - {}.{}".format(
                        series_name,
                        str(season_number).zfill(2),
                        str(episode_number).zfill(2),
                        self._load_tvdb_episode_name(
                            tvdb_id, season_number, episode_number
                        ),
                        ext
                    )
                else:

                    episode_names = []
                    while episode_number < end:
                        episode_names.append(self._load_tvdb_episode_name(
                            tvdb_id, season_number, episode_number
                        ))
                        episode_number += 1
                    episode_names = " | ".join(episode_names)

                    new_name = "{} - S{}E{}-E{} - {}.{}".format(
                        series_name,
                        str(season_number).zfill(2),
                        str(start).zfill(2),
                        str(end).zfill(2),
                        episode_names,
                        ext
                    )

                operations.append(RenameOperation(
                    episode_file,
                    os.path.join(os.path.dirname(episode_file), new_name)
                ))

                episode_number += 1

        return operations

    @staticmethod
    def _load_tvdb_episode_name(
            tvdb_id: str,
            season_number: int,
            episode_number: int
    ) -> str:
        """
        Loads an episode name from TVDB
        :param tvdb_id: The TVDB ID for the episode's series
        :param season_number: The season number
        :param episode_number: The episode number
        :return: The TVDB name
        """
        try:
            tvdb = tvdb_api.Tvdb()
            return tvdb[tvdb_id][season_number][episode_number]["episodename"]

        except (tvdb_episodenotfound, tvdb_seasonnotfound,
                tvdb_shownotfound, ConnectionError, KeyError) as e:
            # If not found, or other error, just return generic name
            if str(e) == "cache_location":  # pragma: no cover
                print("TheTVDB.com is down!")

            return "Episode " + str(episode_number)

    @staticmethod
    def _get_ext(filename: str) -> Optional[str]:
        """
        Gets the file extension of a file
        :param filename: The filename for which to get the file extension
        :return: The file extension or None if the file has no extension
        """
        try:
            return filename.rsplit(".", 1)[1]
        except IndexError:
            return None
