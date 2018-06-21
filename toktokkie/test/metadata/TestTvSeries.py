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

from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.test.metadata.MetadataTester import MetadataTester


class TestTvSeries(MetadataTester):
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