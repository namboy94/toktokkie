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
from typing import List
from unittest.mock import patch
from toktokkie.exceptions import InvalidDirectoryState
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.enums import IdType
from toktokkie.test.TestFramework import _TestFramework


class TestPrompter(_TestFramework):
    """
    Class that tests core functionality of the Prompter class
    """

    def test_too_few_ids(self):
        """
        Tests that too few provided IDs are handled correctly during prompting
        :return: None
        """
        with patch("builtins.input", side_effect=[
            "",  # tags
            "[]", "", "", "", "",  # first round IDs
            "100", "", "", "", "",  # second round IDs
            "", "", "", "", ""  # Season IDs
        ]):
            test_dir = self.get("Tester")
            os.makedirs(os.path.join(test_dir, "Season 1"))
            meta = Tv.prompt(test_dir)
            self.assertEqual(meta["ids"]["tvdb"], ["100"])

    def test_required_ids(self):
        """
        Tests if required IDs are enforced correctly
        :return: None
        """
        class Dummy(Tv):
            @classmethod
            def required_id_types(cls) -> List[IdType]:
                return [IdType.IMDB]

        with patch("builtins.input", side_effect=[
            "",  # tags
            "1",  # tvdb ID,
            "", "", "", "100",  # imdb ID
            "", "", "",  # rest of the IDs
            "", "", "", "", ""  # Season IDs
        ]):
            test_dir = self.get("Tester")
            os.makedirs(os.path.join(test_dir, "Season 1"))
            meta = Dummy.prompt(test_dir)
            self.assertEqual(meta["ids"]["tvdb"], ["1"])
            self.assertEqual(meta["ids"]["imdb"], ["100"])

    def test_pre_prompt_checks(self):
        """
        Tests pre-prompt checking
        :return: None
        """
        new_series = self.get("New Series")
        self.assertFalse(os.path.exists(new_series))

        try:
            Tv.prompt(new_series)
            self.fail()
        except InvalidDirectoryState:
            pass
