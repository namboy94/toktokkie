"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

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
"""

import os
import shutil
import unittest
from unittest import mock
from toktokkie.metadata.Base import Base
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.metadata.types.TvSeriesSeason import TvSeriesSeason


class MetadataGenerationUnitTests(unittest.TestCase):
    """
    Unit tests for the metadata generation
    """

    testdir = "testdir"
    testjson = os.path.join(testdir, "test.json")

    def setUp(self):
        """
        Creates the test directory after deleting any previously existing ones
        :return: None
        """
        self.tearDown()
        os.makedirs("testdir")

    def tearDown(self):
        """
        Deletes all test directories
        :return: None
        """
        if os.path.isdir("testdir"):
            shutil.rmtree("testdir")

    def test_defaults_base_metadata(self):
        """
        Tests the metadata generation of the Base class when providing
        default values
        :return: None
        """
        with mock.patch("builtins.input", return_value=""):
            metadata = Base.generate_from_prompts(self.testdir)

        self.assertEqual(
            metadata.to_json(),
            {"type": "base", "name": "testdir", "tags": []}
        )

    def test_generating_and_reading_base_metadata(self):
        """
        Tests generating and reading a Base metadata object
        :return: None
        """
        user_input = ["TestName", "Tag1,Tag2"]
        with mock.patch("builtins.input", side_effect=user_input):
            metadata = Base.generate_from_prompts(self.testdir)

        self.assertEqual(metadata.type.to_json(), "base")
        self.assertEqual(metadata.name.to_json(), "TestName")
        self.assertEqual(metadata.tags.to_json(), ["Tag1", "Tag2"])

        self.assertEqual(metadata.to_json(), {
            "type": "base", "name": "TestName", "tags": ["Tag1", "Tag2"]
        })
        metadata.write(self.testjson)
        written = Base.from_json_file(self.testjson)

        self.assertEqual(metadata.to_json(), written.to_json())
        self.assertTrue(os.path.isfile(self.testjson))

    def test_defaults_tv_series_metadata(self):
        """
        Tests the metadata generation of the TvSeries class when providing
        default values
        :return: None
        """
        os.makedirs(os.path.join(self.testdir, "Season 1"))
        os.makedirs(os.path.join(self.testdir, "Season 2"))
        os.makedirs(os.path.join(self.testdir, "Season 3"))

        user_input = [
            "Tester", "One, Two",
            "", "a", "a1", "", "123", "", "", "",
            "Two", "124", "ger", "ger", "1280x720",
            "", "125", "1", "test", "", "1", "test", "", "1280p", "test", "",
            "A", "1", "", ""
        ]
        with mock.patch("builtins.input", side_effect=user_input):
            metadata = TvSeries.generate_from_prompts(self.testdir)

        self.assertEqual(metadata.to_json(), {
            "type": "tv_series",
            "name": "Tester",
            "tags": ["One", "Two"],
            "seasons": [
                {
                    "path": "Season 1",
                    "name": "Season 1",
                    "tvdb_ids": [123],
                    "audio_langs": ["eng"],
                    "subtitle_langs": [],
                    "resolutions": [{"x": 1920, "y": 1080}]
                },
                {
                    "path": "Season 2",
                    "name": "Two",
                    "tvdb_ids": [124],
                    "audio_langs": ["ger"],
                    "subtitle_langs": ["ger"],
                    "resolutions": [{"x": 1280, "y": 720}]
                },
                {
                    "path": "Season 3",
                    "name": "Season 3",
                    "tvdb_ids": [125],
                    "audio_langs": ["ger"],
                    "subtitle_langs": ["ger"],
                    "resolutions": [{"x": 1280, "y": 720}]
                }
            ],
            "tvdb_excludes": [],
            "tvdb_irregular_season_starts": []
        })

    def test_generating_and_reading_tv_series_metadata(self):
        """
        Tests generating and readin a TvSeries Metadata object
        :return: None
        """
        os.makedirs(os.path.join(self.testdir, "Season 1"))
        user_input = [
            "Tester", "One, Two",
            "First", "123", "JPN,eng", "gEr", "1280x720",
            "S01E01", "S00E00, S02E10"
        ]

        with mock.patch("builtins.input", side_effect=user_input):
            metadata = TvSeries.generate_from_prompts(self.testdir)

        metadata = metadata  # type: TvSeries

        self.assertEqual(metadata.type.to_json(), "tv_series")
        self.assertEqual(metadata.name.to_json(), "Tester")
        self.assertEqual(metadata.tags.to_json(), ["One", "Two"])
        self.assertEqual(len(metadata.seasons.list), 1)

        season = metadata.seasons.list[0]  # type: TvSeriesSeason

        self.assertEqual(season.path.to_json(), "Season 1")
        self.assertEqual(season.name.to_json(), "First")
        self.assertEqual(season.tvdb_ids.to_json(), [123])
        self.assertEqual(season.audio_langs.to_json(), ["jpn", "eng"])
        self.assertEqual(season.subtitle_langs.to_json(), ["ger"])
        self.assertEqual(season.resolutions.to_json(), [{"x": 1280, "y": 720}])

        self.assertEqual(metadata.tvdb_excludes.to_json(), [{"S": 1, "E": 1}])
        self.assertEqual(
            metadata.tvdb_irregular_season_starts.to_json(),
            [{"S": 0, "E": 0}, {"S": 2, "E": 10}]
        )

        self.assertEqual(metadata.to_json(), {
            "type": "tv_series",
            "name": "Tester",
            "tags": ["One", "Two"],
            "seasons": [{
                "path": "Season 1",
                "name": "First",
                "tvdb_ids": [123],
                "audio_langs": ["jpn", "eng"],
                "subtitle_langs": ["ger"],
                "resolutions": [{"x": 1280, "y": 720}]
            }],
            "tvdb_excludes": [{"S": 1, "E": 1}],
            "tvdb_irregular_season_starts": [
                {"S": 0, "E": 0},
                {"S": 2, "E": 10}
            ]
        })

        metadata.write(self.testjson)
        written = TvSeries.from_json_file(self.testjson)

        self.assertEqual(metadata.to_json(), written.to_json())
        self.assertTrue(os.path.isfile(self.testjson))
