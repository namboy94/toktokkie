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

from toktokkie.neometadata.comic.Comic import Comic
from toktokkie.test.TestFramework import _TestFramework


class TestValidatingComicMetadata(_TestFramework):
    """
    Class that tests the ComicVaildator class
    """

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        valid_data = [
            {"type": "comic", "ids": {"anilist": ["106988"]}}
        ]
        invalid_data = [
            {},
            {"type": "comic"},
            {"type": "comic", "ids": {}},
            {"type": "comic", "ids": {"anilist": 1}},
            {"type": "comic", "ids": {"anilist": [1]}},
            {"type": "comic", "ids": {"anilist": "106988"}},
            {"type": "comic", "ids": {"tvdb": ["106988"]}},
            {"type": "tv_series", "ids": {"anilist": ["106988"]}}
        ]
        self.perform_json_validation(Comic, valid_data, invalid_data)
