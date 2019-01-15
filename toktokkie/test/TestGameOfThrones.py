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
import shutil
import unittest
from toktokkie.Directory import Directory


class TestGameOfThrones(unittest.TestCase):
    """
    Test class that tests the 'Game of Thrones' test directory
    """

    @staticmethod
    def cleanup():
        """
        Deletes any generates resources
        :return:
        """
        if os.path.exists("test-res"):
            shutil.rmtree("test-res")

    def setUp(self):
        """
        Sets up the test resources
        :return: None
        """
        self.cleanup()
        try:
            shutil.copytree("toktokkie/test/res", "test-res")
        except FileNotFoundError:
            shutil.copytree("res", "test-res")

    def tearDown(self):
        """
        Deletes the test resources
        :return: None
        """
        self.cleanup()

    def test_renaming(self):
        """
        Tests renaming the contents of the Game of Thrones directory
        :return: None
        """

        directory = Directory("test-res/Game of Thrones")
        directory.rename(noconfirm=True)

        for mode, data in {
            True: {
                "Season 1": [
                    "S01E01 - Winter Is Coming.txt",
                    "S01E09-E10 - Baelor | Fire and Blood.txt"
                ],
                "Season 2": [
                    "S02E03 - What is Dead May Never Die.txt"
                ],
                "Season 3": [
                    "S03E01 - No Mas.txt"
                ],
                "Other": [
                    "S00E02 - 15-Minute Preview.txt"
                ]
            },
            False: {
                "Season 1": [
                    "S01E07 - You Win or You Die.txt"
                ]
            }
        }.items():

            for season, episodes in data.items():
                for episode in episodes:

                    got = "Game of Thrones"
                    episode_file = "test-res/{}/{}/{} - {}".format(
                        got, season, got, episode
                    )
                    self.assertEqual(
                        mode,
                        os.path.isfile(episode_file)
                    )
