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
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.enums import IdType
from toktokkie.test.TestFramework import _TestFramework


class TestMetadataAddCommand(_TestFramework):
    """
    Class that tests the metadata-add command
    """

    def test_invalid_directory_for_mode(self):
        """
        Tests using an incorrect directory for the metadata-add mode
        :return: None
        """
        path = self.get("Faust")
        self.execute_command(
            ["metadata-add", path, "season", "Season 2"],
            []
        )
        path = self.get("NonExisting")
        self.execute_command(
            ["metadata-add", path, "season", "Season 2"],
            []
        )

    def test_adding_season(self):
        """
        Tests adding a season to a tv metadata
        :return: None
        """
        path = self.get("Over the Garden Wall")
        season_path = os.path.join(path, "Season 2")
        self.assertFalse(os.path.isdir(season_path))
        self.execute_command(
            ["metadata-add", path, "season", "Season 2"],
            ["", "200", "300", "", ""]
        )
        meta = Tv(path)
        self.assertEqual(len(meta.seasons), 2)
        season_2 = meta.seasons[1]
        self.assertEqual(season_2.ids[IdType.TVDB], meta.ids[IdType.TVDB])
        self.assertEqual(season_2.ids[IdType.IMDB], ["200"])
        self.assertEqual(season_2.ids[IdType.MYANIMELIST], ["300"])
        self.assertTrue(os.path.isdir(season_path))

    def test_adding_existing_season(self):
        """
        Tests adding a season to a tv metadata that already exists
        :return: None
        """
        path = self.get("Over the Garden Wall")
        self.execute_command(
            ["metadata-add", path, "season", "Season 1"],
            []
        )
        meta = Tv(path)
        self.assertEqual(len(meta.seasons), 1)

    def test_adding_exclude(self):
        """
        Tests adding a tv metadata exclude
        :return: None
        """
        path = self.get("Over the Garden Wall")
        self.execute_command(
            ["metadata-add", path, "exclude", "imdb", "1", "5"],
            []
        )
        meta = Tv(path)
        self.assertEqual(
            meta.excludes[IdType.IMDB],
            {1: [5]}
        )

    def test_adding_multi_episode(self):
        """
        Tests adding a tv metadata multi episde
        :return: None
        """
        path = self.get("Over the Garden Wall")
        self.execute_command(
            ["metadata-add", path, "multi-episode", "imdb", "1", "5", "7"],
            []
        )
        meta = Tv(path)
        self.assertEqual(
            meta.multi_episodes[IdType.IMDB],
            {1: {5: 7}}
        )
