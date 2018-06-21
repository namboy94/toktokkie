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
from toktokkie.metadata.types.AgentIdType import AgentIdType
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.test.metadata.TestBase import TestBase


class TestTvSeries(TestBase):
    """
    Class that contains tests for the TvSeries Metadata class
    """

    metadata_cls = TvSeries
    """
    The metadata class to test. Used by helper methods defined here
    """

    json_data_example = {
        "type": "tv_series",
        "name": "TestTvSeries",
        "tags": ["Tag1", "Tag2", "Tag3"],
        "seasons": [
            {
                "path": "Season 1",
                "name": "Season 1",
                "tvdb_ids": [12345],
                "audio_langs": ["eng"],
                "subtitle_langs": ["eng", "ger"],
                "resolutions": [{"x": 1920, "y": 1080}]
            },
            {
                "path": "Season 2",
                "name": "Season 2",
                "tvdb_ids": [12345],
                "audio_langs": ["eng"],
                "subtitle_langs": ["eng", "ger"],
                "resolutions": [{"x": 1920, "y": 1080}]
            },
            {
                "path": "Specials",
                "name": "Specials",
                "tvdb_ids": [54321, 12345],
                "audio_langs": ["fre"],
                "subtitle_langs": ["jpn"],
                "resolutions": [{"x": 1280, "y": 720}, {"x": 1920, "y": 1080}]
            }
        ],
        "tvdb_excludes": [{"S": 0, "E": 1}, {"S": 0, "E": 2}],
        "tvdb_irregular_season_starts": [{"S": 0, "E": 0}, {"S": 1, "E": 2}],
        "tvdb_multi_episodes": [
            {"start": {"S": 1, "E": 3}, "end": {"S": 1, "E": 4}},
            {"start": {"S": 1, "E": 5}, "end": {"S": 1, "E": 10}}
        ]

    }
    """
    An example metadata dictionary. Used to test generating the metadata
    object using a constructor call
    """

    user_input_example = [
        "TestTvSeries",
        "Tag1,Tag2,Tag3",
        "Season 1",
        "12345",
        "eng",
        "eng,ger",
        "1920x1080",
        "", "", "", "", "",  # Season 2 with autocomplete
        "Specials",
        "54321,12345",
        "fre",
        "jpn",
        "1280x720, 1920x1080",
        "S00E01,S00E02",
        "S00E00,S01E02",
        "S01E03-04,S01E05-10"
    ]
    """
    Example user input that generates the same metadata as
    the json_data_example.
    """

    subdirectories = ["Season 1", "Season 2", "Specials"]
    """
    A list of subdirectory names to generate during setup
    """

    def test_getting_season_start(self):
        """
        Tests retrieving the episode at which a season starts
        :return: None
        """
        metadata = self.generate_metadata()  # type: TvSeries
        self.assertEqual(metadata.get_season_start(AgentIdType.TVDB, 1), 2)
        self.assertEqual(metadata.get_season_start(AgentIdType.TVDB, 2), 1)
        self.assertEqual(metadata.get_season_start(AgentIdType.TVDB, 0), 0)

    def test_getting_excludes(self):
        """
        Tests retrieving excluded episodes
        :return: None
        """
        metadata = self.generate_metadata()  # type: TvSeries
        ranges = metadata.get_multi_episode_ranges(AgentIdType.TVDB)

        expected = [
            {"S": 0, "E": 1}, {"S": 0, "E": 2}
        ]
        for _range in ranges:
            while _range["start"]["E"] != _range["end"]["E"]:
                _range["start"]["E"] += 1
                expected.append(_range["start"].copy())

        for excluded in metadata.get_agent_excludes(AgentIdType.TVDB):
            self.assertTrue(excluded in expected)

    def test_using_unsupported_agent_type(self):
        """
        Tests using an unsupported agent type
        :return: None
        """
        metadata = self.generate_metadata()  # type: TvSeries
        self.assertEqual(
            metadata.get_season_start(AgentIdType.MYANIMELIST, 1),
            1
        )
        self.assertEqual(
            metadata.get_multi_episode_ranges(AgentIdType.MYANIMELIST),
            None
        )
        self.assertEqual(
            metadata.get_agent_excludes(AgentIdType.MYANIMELIST),
            None
        )

    def test_generating_from_user_prompts_with_hidden_dirs_and_files(self):
        """
        Tests generating a metadata object where hidden directories and files
        exist in the media directory
        :return: None
        """
        check = self.generate_metadata(self.user_input_example)
        with open(os.path.join(self.testdir, "file.txt"), "w") as f:
            f.write("test")
        os.makedirs(os.path.join(self.testdir, ".test"))
        new = self.generate_metadata(self.user_input_example)
        self.assertEqual(new.to_json(), check.to_json())
