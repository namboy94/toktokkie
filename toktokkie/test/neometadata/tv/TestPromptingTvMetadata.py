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
from toktokkie.exceptions import InvalidDirectoryState
from toktokkie.neometadata.tv.Tv import Tv
from toktokkie.neometadata.enums import IdType
from toktokkie.Directory import Directory
from toktokkie.test.TestFramework import _TestFramework


class TestPromptingTvMetadata(_TestFramework):
    """
    Class that tests generating tv series metadata
    """

    def test_prompt(self):
        ngnl = self.get("No Game No Life")
        os.makedirs(ngnl)
        os.makedirs(os.path.join(ngnl, "Season 1"))
        os.makedirs(os.path.join(ngnl, "Movie"))
        with mock.patch("builtins.input", side_effect=[
            "anime, no_second_season",  # tags
            "278155",  # TVDB ID
            "",  # IMDB ID
            "19815",  # MAL ID
            "",  # Anilist ID
            "",  # Kitsu ID
            "",  # S1 TVDB ID
            "",  # S1 IMDB ID
            "",  # S1 MAL ID
            "",  # S1 Anilist ID
            "",  # S1 Kitsu ID
            "",  # Movie TVDB ID
            "",  # Movie IMDB ID
            "33674",  # Movie MAL ID
            "",  # Movie Anilist ID
            ""  # Movie Kitsu ID
        ]):
            metadata = Tv.from_prompt(ngnl)
            metadata.write()

        self.assertTrue(os.path.isdir(metadata.directory_path))
        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata, Directory(metadata.directory_path).metadata)
        self.assertEqual(metadata.ids[IdType.TVDB], ["278155"])
        self.assertEqual(metadata.ids[IdType.ANILIST], ["19815"])
        self.assertEqual(metadata.ids[IdType.MYANIMELIST], ["19815"])
        self.assertEqual(metadata.ids[IdType.KITSU], [])

        season_one = metadata.get_season("Season 1")
        movie = metadata.get_season("Movie")

        self.assertEqual(season_one.ids[IdType.TVDB], ["278155"])
        self.assertEqual(season_one.ids[IdType.ANILIST], ["19815"])
        self.assertEqual(season_one.ids[IdType.MYANIMELIST], ["19815"])
        self.assertEqual(season_one.ids[IdType.KITSU], [])
        self.assertEqual(movie.ids[IdType.TVDB], ["278155"])
        self.assertEqual(movie.ids[IdType.ANILIST], ["21875"])
        self.assertEqual(movie.ids[IdType.MYANIMELIST], ["33674"])
        self.assertEqual(movie.ids[IdType.KITSU], [])

        for invalid in [
            IdType.VNDB, IdType.MANGADEX, IdType.ISBN
        ]:
            self.assertFalse(invalid in metadata.ids)

        for tag in ["anime", "no_second_season"]:
            self.assertTrue(tag in metadata.tags)

    def test_catching_special_season(self):
        """
        Makes sure that special seasons that start with "Season" are
        handled correctly
        """

        ngnl = self.get("No Game No Life")
        os.makedirs(ngnl)
        os.makedirs(os.path.join(ngnl, "Season X"))
        with mock.patch("builtins.input", side_effect=[
            "",  # tags
            "278155",  # TVDB ID
            "", "", "", "",  # Other IDs
            "", "", "", "", ""  # Season X Ids
        ]):
            metadata = Tv.from_prompt(ngnl)
            metadata.write()

        self.assertTrue(os.path.isdir(metadata.directory_path))
        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertTrue(os.path.isfile(metadata.metadata_file))

    def test_pre_prompt_checks(self):
        """
        Tests pre-prompt checking
        :return: None
        """
        new_series = self.get("New Series")
        os.makedirs(new_series)

        try:
            Tv.prompt(new_series)
            self.fail()
        except InvalidDirectoryState:
            pass
