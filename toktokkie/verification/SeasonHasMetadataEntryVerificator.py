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
from toktokkie.verification.Verificator import Verificator
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.metadata.AnimeSeries import AnimeSeries
from toktokkie.metadata.types.TvSeriesSeason import TvSeriesSeason
from toktokkie.metadata.types.AnimeSeriesSeason import AnimeSeriesSeason


class SeasonHasMetadataEntryVerificator(Verificator):
    """
    Verificator that makes sure that each subdirectory/season not starting
    with a '.' is represented in the metadata
    """

    applicable_metadata_types = [TvSeries]
    """
    Metadata classes on which this verificator may be executed on
    Also applicable to children of those classes
    """

    dirs_without_entry = []
    """
    Stores any icons that were identified as missing
    """

    def verify(self) -> bool:
        """
        Checks if all required icon files exist
        :return: True if all icons are present, False if one is missing
        """
        metadata = self.directory.metadata  # type: TvSeries

        if not metadata.is_subclass_of(TvSeries):
            return True

        missing = False

        for subdirectory in os.listdir(self.directory.path):

            path = os.path.join(self.directory.path, subdirectory)
            if subdirectory.startswith(".") or not os.path.isdir(path):
                continue

            filtered = list(filter(
                lambda x: x.path == subdirectory, metadata.seasons.list
            ))

            if len(filtered) == 0:
                missing = True
                self.dirs_without_entry.append(subdirectory)

        return not missing

    def fix(self):
        """
        Allows the user to fix missing icons by saving an icon file
        to the correct location
        :return: None
        """
        metadata = self.directory.metadata  # type: TvSeries
        seasons = metadata.seasons.list
        previous = None

        if len(seasons) >= 1:
            season_type = type(seasons[0])  # type: TvSeriesSeason
            previous = seasons[len(seasons) - 1]
        elif metadata.type == TvSeries.type:
            season_type = TvSeriesSeason
        elif metadata.type == AnimeSeries.type:
            season_type = AnimeSeriesSeason
        else:
            self.print_err("Not implemented")
            sys.exit(1)

        for subdirectory in self.dirs_without_entry:
            season_type.prompt(subdirectory, previous)
