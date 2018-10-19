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
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.components import MovieIdType


class Movie(Metadata):
    """
    Metadata class that model a Movie
    """

    @classmethod
    def id_type(cls) -> type(MovieIdType):
        """
        :return: The ID type used by this metadata object
        """
        return MovieIdType

    @classmethod
    def media_type(cls) -> str:
        """
        :return: The media type of the Metadata class
        """
        return "movie"

    @classmethod
    def prompt(cls, directory_path: str) -> Metadata:
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        print("Generating metadata for {}:"
              .format(os.path.basename(directory_path)))
        return cls(directory_path, {"ids": cls.prompt_for_ids()})
