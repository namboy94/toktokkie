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

from toktokkie.metadata.AnimeMovie import AnimeMovie
from toktokkie.test.metadata.MetadataTester import MetadataTester


class TestAnimeMovie(MetadataTester):
    """
    Class that contains tests for the AnimeMovie Metadata class
    """

    metadata_cls = AnimeMovie
    """
    The metadata class to test. Used by helper methods defined here
    """

    json_data_example = {
        "type": "anime_movie",
        "name": "TestAnimeMovie",
        "tags": ["Tag1", "Tag2", "Tag3"],
        "imdb_id": "tt10101010",
        "resolution": {"x": 1920, "y": 1080},
        "audio_langs": ["eng", "ger"],
        "subtitle_langs": ["fre", "spa"],
        "mal_id": 10000
    }
    """
    An example metadata dictionary. Used to test generating the metadata
    object using a constructor call
    """

    user_input_example = [
        "TestAnimeMovie",
        "Tag1,Tag2,Tag3",
        "tt10101010",
        "1920x1080",
        "eng,ger",
        "fre,spa",
        "10000"
    ]
    """
    Example user input that generates the same metadata as
    the json_data_example.
    """
