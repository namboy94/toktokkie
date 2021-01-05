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
from unittest.mock import patch
from toktokkie.Directory import Directory
from toktokkie.enums import IdType, MediaType
from toktokkie.test.TestFramework import _TestFramework
from toktokkie.metadata.base.Renamer import Renamer


class TestRenamer(_TestFramework):
    """
    Class that tests core functionality of the Renamer class
    """

    def test_skipping_title_rename(self):
        """
        Tests skipping renaming the title
        :return: None
        """
        otgw = self.get("Over the Garden Wall")
        otgw_dir = Directory(otgw)

        otgw_dir.metadata.set_ids(IdType.ANILIST, ["19815"])
        otgw_dir.rename(noconfirm=True, skip_title=True)

        self.assertEqual(otgw_dir.metadata.name, "Over the Garden Wall")
        self.assertTrue(otgw_dir.path.endswith("Over the Garden Wall"))
        self.assertTrue(
            otgw_dir.metadata.directory_path.endswith("Over the Garden Wall")
        )
        self.assertTrue(os.path.isfile(os.path.join(
            otgw_dir.path,
            "Season 1",
            "Over the Garden Wall - S01E01 - Chapter 1; "
            "The Old Grist Mill.mkv",
        )))

        self.assertNotEqual(otgw_dir.metadata.name, "No Game, No Life")
        self.assertFalse(otgw_dir.path.endswith("No Game, No Life"))
        self.assertFalse(
            otgw_dir.metadata.directory_path.endswith("No Game, No Life")
        )
        self.assertFalse(os.path.isfile(os.path.join(
            otgw_dir.path,
            "Season 1",
            "No Game, No Life - S01E01 - Chapter 1; The Old Grist Mill.mkv",
        )))

    def test_renaming_prompts(self):
        otgw = self.get("Over the Garden Wall")
        otgw_dir = Directory(otgw)
        otgw_dir.metadata.set_ids(IdType.ANILIST, ["19815"])

        correct, wrong = self.scramble_episode_names(otgw)

        with patch("builtins.input", side_effect=["n", "n"]):
            otgw_dir.rename()

        for _file in correct:
            self.assertFalse(os.path.isfile(_file))
        for _file in wrong:
            self.assertTrue(os.path.isfile(_file))

        with patch("builtins.input", side_effect=["n", "y"]):
            otgw_dir.rename()

        for _file in correct:
            self.assertTrue(os.path.isfile(_file))
        for _file in wrong:
            self.assertFalse(os.path.isfile(_file))

    def test_anilist_title_loading(self):
        """
        Tests loading the title using anilist
        :return: None
        """
        self.assertEqual(
            Renamer.load_anilist_title_and_year(["0"], MediaType.TV_SERIES),
            None
        )

        self.assertEqual(
            Renamer.load_anilist_title_and_year(["1"], MediaType.TV_SERIES),
            ("Cowboy Bebop", 1998)
        )

        self.assertEqual(
            Renamer.load_anilist_title_and_year(["86635"], MediaType.COMIC),
            ("Kaguya-sama; Love is War", 2015)
        )

    def test_imdb_title_loading(self):
        """
        Tests loading the title using myanimelist
        :return: None
        """
        self.assertEqual(
            Renamer.load_imdb_title_and_year(["0"]),
            None
        )
        self.assertEqual(
            Renamer.load_imdb_title_and_year(["tt0944947"]),
            ("Game of Thrones", 2011)
        )

    def test_title_loader_fallback(self):
        """
        Tests if the title loader correctly falls back on the current name if
        no IDs are available
        :return: None
        """

        # noinspection PyAbstractClass
        class Dummy(Renamer):
            ids = {}
            name = "Unknown"

        renamer = Dummy()
        self.assertEqual(
            renamer.load_title_and_year([IdType.KITSU]),
            ("Unknown", None)
        )
