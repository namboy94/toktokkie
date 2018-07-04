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
from typing import List
from toktokkie.verification.Verificator import Verificator
from toktokkie.metadata.TvSeries import TvSeries, TvSeriesSeason


class SeasonMetadataVerificator(Verificator):
    """
    Verificator that makes sure that each subdirectory/season not starting
    with a '.' is represented in the metadata and every entry in the
    metadata has a corresponding directory
    """

    applicable_metadata_types = [TvSeries]
    """
    Metadata classes on which this verificator may be executed on
    Also applicable to children of those classes
    """

    def _verify(self) -> bool:
        """
        Checks if all required directories and metadata entries are present
        :return: True if all directories and entries are present, else False
        """
        dirs_without_entries = len(self.__get_dirs_without_entries())
        entries_without_dirs = len(self.__get_entries_without_dirs())
        return dirs_without_entries + entries_without_dirs <= 0

    def fix(self):
        """
        Allows the user to fix missing metadata entries using prompts.
        Missing directories are generated automatically without manual input
        to the correct location
        :return: None
        """
        dirs_without_entries = self.__get_dirs_without_entries()
        entries_without_dirs = self.__get_entries_without_dirs()

        if len(dirs_without_entries) > 0:

            self.print_err("Metadata entries missing.")
            self.print_ins("Please enter the missing data:")

            metadata = self.directory.metadata  # type: TvSeries
            season_type = metadata.season_type

            try:
                previous = metadata.seasons.list[0]
            except IndexError:
                previous = None

            for subdirectory in self.__get_dirs_without_entries():
                previous = season_type.prompt(subdirectory, previous)
                self.directory.metadata.seasons.append(previous)

            self.directory.write_metadata()

        if len(entries_without_dirs) > 0:

            self.print_err("Directories present in metadata missing")
            self.print_inf("Directories are being generated...")

            for directory in entries_without_dirs:
                self.print_inf(directory)
                os.makedirs(directory)

            self.print_inf("Done.")

    def __get_dirs_without_entries(self) -> List[str]:
        """
        Retrieves any directories without a metadata entry
        :return: A list of directory names without metadata entries
        """
        metadata = self.directory.metadata  # type: TvSeries
        dirs_without_entry = []

        for subdirectory in os.listdir(self.directory.path):

            path = os.path.join(self.directory.path, subdirectory)
            if subdirectory.startswith(".") or not os.path.isdir(path):
                continue

            # Note: x.path is not the same as the above path variable
            filtered = list(filter(
                lambda x: x.path == subdirectory, metadata.seasons.list
            ))

            if len(filtered) == 0:
                dirs_without_entry.append(subdirectory)

        return dirs_without_entry

    def __get_entries_without_dirs(self) -> List[str]:
        """
        Searches for metadata entries without corresponding directories
        :return: A list of paths at which directories were expected
        """
        metadata = self.directory.metadata  # type: TvSeries
        entries_without_metadata = []

        for season in metadata.seasons.list:  # type: TvSeriesSeason
            expected = os.path.join(self.directory.path, season.path)

            if not os.path.isdir(expected):
                entries_without_metadata.append(expected)

        return entries_without_metadata
