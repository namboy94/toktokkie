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
from puffotter.os import listdir, get_ext
from toktokkie.enums import IdType
from toktokkie.metadata.base.Renamer import Renamer
from toktokkie.metadata.book.BookExtras import BookExtras
from toktokkie.metadata.base.components.RenameOperation import RenameOperation


class BookRenamer(Renamer, BookExtras, ABC):
    """
    Implements the Renamer functionality for book metadata
    """

    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Creates renaming operations for book metadata
        :return: The renaming operations
        """
        book_files = listdir(self.directory_path, no_dirs=True)
        book_file, path = book_files[0]
        return [RenameOperation(path, f"{self.name}.{get_ext(book_file)}")]

    def resolve_title_name(self) -> str:
        """
        If possible, will fetch the appropriate name for the
        metadata based on IDs, falling back to the
        directory name if this is not possible or supported.
        """
        return self.load_title_and_year([
            IdType.ANILIST
        ])[0]
