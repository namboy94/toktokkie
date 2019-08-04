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
from tvdb_api import tvdb_episodenotfound, tvdb_seasonnotfound, \
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
        # Visual Novels don't get renamed!
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
        dest = "{}.{}".format(self.metadata.name, self.get_ext(book_file))
        return [RenameOperation(
            os.path.join(self.path, book_file), dest
        )]

    def _generate_book_series_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for book series media types
        :return: The list of rename operations
        """
        operations = []
        children = self._get_children(no_dirs=True)
        fill = len(str(len(children))) + 1

        for i, volume in enumerate(children):
            ext = volume.rsplit(".", 1)[1]
            new_name = "{} - Volume {}.{}".format(
                self.metadata.name,
                str(i + 1).zfill(fill),
                ext
            )

            operations.append(RenameOperation(
                os.path.join(self.path, volume), new_name
            ))

        return operations

    def _generate_movie_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for movie media types
        :return: The list of rename operations
        """
        movie_file = self._get_children(no_dirs=True)[0]
        dest = "{}.{}".format(self.metadata.name, self.get_ext(movie_file))
        return [RenameOperation(
            os.path.join(self.path, movie_file), dest
        )]

    def _generate_tv_series_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for tv series media types
        :return: The list of rename operations
        """
        operations = []

        # noinspection PyTypeChecker
        tv_series_metadata = self.metadata  # type: TvSeries

        excluded = tv_series_metadata.excludes.get(TvIdType.TVDB, {})
        multis = tv_series_metadata.multi_episodes.get(TvIdType.TVDB, {})
        start_overrides = \
            tv_series_metadata.season_start_overrides.get(TvIdType.TVDB, {})

        content_info = tv_series_metadata.get_episode_files()

        for tvdb_id, season_data in content_info.items():
            is_spinoff = tv_series_metadata.tvdb_id != tvdb_id

            if is_spinoff:
                sample_episode = season_data[list(season_data)[0]][0]
                location = os.path.dirname(sample_episode)
                series_name = os.path.basename(location)
            else:
                series_name = tv_series_metadata.name

            for _season_number, episodes in season_data.items():
                season_number = _season_number if not is_spinoff else 1

                season_excluded = excluded.get(season_number, [])
                season_multis = multis.get(season_number, {})
                episode_number = start_overrides.get(season_number, 1)

                for episode_file in episodes:

                    while episode_number in season_excluded:
                        episode_number += 1

                    if episode_number in season_multis:
                        end = season_multis[episode_number]
                    else:
                        end = None

                    episode_name = self.load_tvdb_episode_name(
                        tvdb_id, season_number, episode_number, end
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
        ext = Renamer.get_ext(original_file)
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
    def load_tvdb_episode_name(
            tvdb_id: str,
            season_number: int,
            episode_number: int,
            multi_end: Optional[int] = None
    ) -> str:
        """
        Loads an episode name from TVDB
        :param tvdb_id: The TVDB ID for the episode's series
        :param season_number: The season number
        :param episode_number: The episode number
        :param multi_end: If provided,
                          will generate a name for a range of episodes
        :return: The TVDB name
        """
        if int(tvdb_id) == 0:
            return "Episode " + str(episode_number)

        if multi_end is not None:
            episode_names = []
            for episode in range(episode_number, multi_end + 1):
                episode_names.append(Renamer.load_tvdb_episode_name(
                    tvdb_id,
                    season_number,
                    episode
                ))
            return " | ".join(episode_names)

        try:
            tvdb = tvdb_api.Tvdb()
            tvdb_id = int(tvdb_id)
            return tvdb[tvdb_id][season_number][episode_number]["episodeName"]

        except (tvdb_episodenotfound, tvdb_seasonnotfound,
                tvdb_shownotfound, ConnectionError, KeyError) as e:
            # If not found, or other error, just return generic name
            if str(e) == "cache_location":  # pragma: no cover
                print("TheTVDB.com is down!")

            return "Episode " + str(episode_number)

    @staticmethod
    def get_ext(filename: str) -> Optional[str]:
        """
        Gets the file extension of a file
        :param filename: The filename for which to get the file extension
        :return: The file extension or None if the file has no extension
        """
        try:
            return filename.rsplit(".", 1)[1]
        except IndexError:
            return None
