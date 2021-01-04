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
from toktokkie.neometadata.utils.RenameOperation import RenameOperation
from toktokkie.neometadata.enums import IdType
from toktokkie.neometadata.base.Renamer import Renamer
from toktokkie.neometadata.movie.MovieExtras import MovieExtras


class MovieRenamer(Renamer, MovieExtras, ABC):
    """
    Implements the Renamer functionality for movie metadata
    """

    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Creates renaming operations for movie metadata
        :return: The renaming operations
        """
        movie_name, movie_path = listdir(self.directory_path, no_dirs=True)[0]
        new_name = f"{self.name}.{get_ext(movie_name)}"
        return [RenameOperation(movie_path, new_name)]

    def resolve_title_name(self) -> str:
        """
        If possible, will fetch the appropriate name for the
        metadata based on IDs, falling back to the
        directory name if this is not possible or supported.
        """
        name, year = self.load_title_and_year([
            IdType.IMDB,
            IdType.ANILIST
        ])
        if year is None:
            return self.name
        else:
            return f"{name} ({year})"
