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
from unittest import mock
from toktokkie.Directory import Directory
from toktokkie.metadata.types.Movie import Movie
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.test.metadata.TestMetadata import _TestMetadata


class TestMovie(_TestMetadata):
    """
    Class that tests the Movie metadata class
    """

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        valid_data = [
            {"type": "movie", "ids": {"imdb": ["tt0234215"]}}
        ]
        invalid_data = [
            {},
            {"type": "movie"},
            {"type": "movie", "ids": {}},
            {"type": "movie", "ids": {"imdb": 100}},
            {"type": "movie", "ids": {"anilist": "100"}},
            {"type": "movie", "ids": {"imdb": [100]}},
            {"type": "movie", "ids": {"isbn": ["100"]}},
            {"type": "movie", "ids": {"imdb": "tt0234215"}},
            {"type": "movie", "ids": {"imdb": "tt0234215", "other": "stuff"}},
            {"type": "movie", "ids": {"imdb": "tt0234215", "tvdb": "stuff"}}
        ]
        matrix = self.get("The Matrix (1999)")
        self.check_validation(valid_data, invalid_data, Movie, matrix)

    def test_checking(self):
        """
        Tests if the checking mechanisms work correctly
        :return: None
        """
        matrix = Directory(self.get("The Matrix (1999)"))
        self.assertTrue(matrix.check(False, False, {}))
        os.remove(os.path.join(matrix.meta_dir, "icons/main.png"))
        self.assertFalse(matrix.check(False, False, {}))
