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
from puffotter.os import listdir
from toktokkie.exceptions import InvalidMetadata
from toktokkie.neometadata.base.Validator import Validator
from toktokkie.neometadata.movie.MovieExtras import MovieExtras


class MovieValidator(Validator, MovieExtras, ABC):
    """
    Implements the Validator functionality for movie metadata
    """

    def validate(self):
        """
        Ensures that the movie file exist
        :return: None
        """
        super().validate()
        if len(listdir(self.directory_path, no_dirs=True)) != 1:
            raise InvalidMetadata("Incorrect amount of movie files")
