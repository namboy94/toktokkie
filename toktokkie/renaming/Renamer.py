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
import sys
from colorama import Fore, Style
from typing import Dict, List
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.metadata.components.enums import MediaType, TvIdType
from toktokkie.renaming.helper.resolve import resolve_season, get_episode_files
from toktokkie.renaming.Episode import Episode
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
            self.operations = self.generate_book_operations()
        elif self.metadata.media_type() == MediaType.BOOK:
            self.operations = self.generate_book_series_operations()
        elif self.metadata.media_type() == MediaType.BOOK:
            self.operations = self.generate_movie_operations()
        elif self.metadata.media_type() == MediaType.BOOK:
            self.operations = self.generate_tv_series_operations()
        else:  # pragma: no cover
            self.operations = []

    def get_children(self, no_dirs: bool = False, no_files: bool = False) \
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

    # noinspection PyMethodMayBeStatic
    def generate_book_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for book media types
        :return: The list of rename operations
        """
        return []

    def generate_book_series_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for book series media types
        :return: The list of rename operations
        """

        operations = []

        for i, volume in enumerate(self.get_children(no_dirs=True)):

            new_name = "{} - Volume {}".format(
                self.metadata.name,
                str(i + 1).zfill(2)
            )

            operations.append(RenameOperation(
                os.path.join(self.path, volume),
                os.path.join(self.path, new_name)
            ))
        return operations

    # noinspection PyMethodMayBeStatic
    def generate_movie_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for movie media types
        :return: The list of rename operations
        """
        return []

    def generate_tv_series_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for tv series media types
        :return: The list of rename operations
        """
        tv_series_metadata = self.metadata  # type: TvSeries
        operations = []

        episodes = self.find_tv_episode_files()
        episodes = self.resolve_tv_episodes(tv_series_metadata, episodes)

    def find_tv_episode_files(self) -> Dict[int, List[str]]:
        """
        Finds all valid episode files inside a tv series media directory
        :return: A dictionary mapping lists of episode files to season numbers
                 Form: {season_number: [epifile1, epifile2]}
        """
        tv_series_metadata = self.metadata  # type: TvSeries
        episodes = {}

        for season in self.get_children(no_files=True):

            try:
                season_metadata = tv_series_metadata.get_season(season)
            except KeyError:
                continue

            if season_metadata.season_number not in episodes:
                episodes[season_metadata.season_number] = []

            for episode in os.listdir(season_metadata.path):
                episode_path = os.path.join(season_metadata.path, episode)

                if not os.path.isfile(episode_path) or episode.startswith("."):
                    continue

                episodes[season_metadata.season_number].append(episode_path)

        return episodes

    def resolve_tv_episodes(self, episode_data: Dict[int, List[str]]) -> Dict[int, List[str]]:

        metadata = self.metadata  # type: TvSeries

        operations = []
        resolved = {}
        excluded = metadata.excludes.get(TvIdType.TVDB, {})
        multis = metadata.multi_episodes.get(TvIdType.TVDB, {})
        start_overrides = \
            metadata.season_start_overrides.get(TvIdType.TVDB, {})


        for season, episodes in episode_data.items():
            episode_count = start_overrides.get(season, 1)

            if season not in excluded:
                excluded[season] = []
            if season not in multis:
                multis[season] = {}

            tvdb_id =

            for episode in sorted(episodes):

                while episode_count in excluded[season]:
                    episode_count += 1











    def parse_directory(self) -> Dict[int, Dict[str, str or List[int]]]:
        """
        Parses the directory provided as self.path, searches for episode
        content. Only files not starting with "." are included
        :return: A dictionary keyed by season, containing information about
                 the season's episodes by name, path and agent IDs
        """

        episodes = {}
        for season in self.metadata.seasons.list:
            season_path = os.path.join(self.path, season.path)
            season_number = resolve_season(season_path)
            season_ids = season.get_agent_ids(self.agent.id_type)

            if season_ids is None:
                raise ValueError("Invalid agent ID type")

            if season_number not in episodes:
                episodes[season_number] = []

            for episode in get_episode_files(season_path):
                episodes[season_number].append({
                    "name": os.path.basename(episode),
                    "path": episode,
                    "agent_ids": season_ids
                })

        return episodes

    def initialize_episodes(self) -> List[Episode]:
        """
        Initializes the episode objects that generate the new name for the
        episodes
        :return: The list of generated Episode objects
        """

        episodes = []

        for season in sorted(self.raw_episodes):

            eps = sorted(self.raw_episodes[season], key=lambda x: x["name"])
            episode_count = \
                self.metadata.get_season_start(self.agent.id_type, season)
            excluded = self.metadata.get_agent_excludes(self.agent.id_type)

            for episode in eps:

                # Skip excluded episodes
                while True:
                    exclude = list(filter(
                        lambda x: x["S"] == season
                        and x["E"] == episode_count,
                        excluded
                    ))
                    if len(exclude) == 0:
                        break
                    else:
                        episode_count += 1

                # Check for multi episodes
                multi_range = None
                for multi_episode in self.metadata.get_multi_episode_ranges(
                        self.agent.id_type
                ):
                    multi_s = multi_episode["start"]["S"]
                    multi_e = multi_episode["start"]["E"]

                    if multi_s == season and multi_e == episode_count:
                        multi_range = (multi_e, multi_episode["end"]["E"])

                # noinspection PyTypeChecker
                episodes.append(Episode(
                    episode["path"],
                    self.metadata.name,
                    episode["agent_ids"],
                    season,
                    episode_count,
                    self.scheme,
                    self.agent,
                    multi_range
                ))

                # Skip multi-episode parts
                if multi_range is not None:
                    episode_count = multi_range[1]

                episode_count += 1

        return episodes

    def rename(self, noconfirm: bool):
        """
        Renames the contained files according to the naming scheme.
        :param noconfirm: Skips the confirmation phase if True
        :return: None
        """

        max_current = \
            len(max(self.episodes, key=lambda x: len(x.current)).current)

        for episode in self.episodes:
            print(Fore.LIGHTCYAN_EX + episode.current.ljust(max_current + 1) +
                  Style.RESET_ALL + " ---> " + Fore.LIGHTYELLOW_EX +
                  episode.new + Style.RESET_ALL)

        if not noconfirm:
            confirm = input("Start the renaming Process? (y/n)")
            if confirm != "y":
                print("Renaming aborted")
                sys.exit(0)

        for episode in self.episodes:
            episode.rename()
