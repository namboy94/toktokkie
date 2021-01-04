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

from typing import List
from toktokkie.neometadata.enums import IdType, MediaType
from toktokkie.neometadata.base.Metadata import Metadata
from toktokkie.neometadata.movie.MoviePrompter import MoviePrompter
from toktokkie.neometadata.movie.MovieRenamer import MovieRenamer
from toktokkie.neometadata.movie.MovieValidator import MovieValidator


class Movie(Metadata, MovieRenamer, MoviePrompter, MovieValidator):
    """
    Metadata class that handles movies
    """

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The Movie media type
        """
        return MediaType.MOVIE

    @classmethod
    def valid_id_types(cls) -> List[IdType]:
        """
        :return: A list of valid ID types
        """
        return [
            IdType.IMDB,
            IdType.MYANIMELIST,
            IdType.ANILIST,
            IdType.KITSU
        ]
