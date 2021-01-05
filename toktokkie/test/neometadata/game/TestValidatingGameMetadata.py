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
from toktokkie.exceptions import InvalidMetadata
from toktokkie.neometadata.game.Game import Game
from toktokkie.test.TestFramework import _TestFramework


class TestValidatingGameMetadata(_TestFramework):
    """
    Class that tests the GameVaildator class
    """

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        valid_data = [
            {"type": "game", "ids": {"vndb": ["100"]}}
        ]
        invalid_data = [
            {},  # Missing type and ids
            {"type": "game"},  # Missing ids
            {"type": "game", "ids": {}},  # 0 IDs
            {"type": "game", "ids": {"vndb": "100"}},  # Ids not a list
            {"type": "game", "ids": {"vndb": 100}},  # Ids not a list
            {"type": "game", "ids": {"vndb": [100]}},  # Ids not string
            {"type": "movie", "ids": {"vndb": ["100"]}}  # Wrong media type
        ]
        self.perform_json_validation(Game, valid_data, invalid_data)
