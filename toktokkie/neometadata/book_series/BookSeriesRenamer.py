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
from typing import List
from puffotter.os import listdir
from toktokkie.neometadata.enums import IdType
from toktokkie.neometadata.utils.RenameOperation import RenameOperation
from toktokkie.neometadata.base.Renamer import Renamer
from toktokkie.neometadata.book_series.BookSeriesExtras import BookSeriesExtras


class BookSeriesRenamer(Renamer, BookSeriesExtras, ABC):
    """
    Implements the Renamer functionality for book series metadata
    """

    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Creates renaming operations for book series metadata
        :return: The renaming operations
        """
        operations = []
        children = listdir(self.directory_path, no_dirs=True)
        fill = len(str(len(children)))

        for i, (volume, path) in enumerate(children):
            ext = volume.rsplit(".", 1)[1]
            new_name = "{} - Volume {}.{}".format(
                self.name,
                str(i + 1).zfill(fill),
                ext
            )

            operations.append(RenameOperation(path, new_name))

        return operations

    def resolve_title_name(self) -> str:
        """
        If possible, will fetch the appropriate name for the
        metadata based on IDs, falling back to the
        directory name if this is not possible or supported.
        """
        return self.load_title_and_year([
            IdType.ANILIST
        ])[0]
