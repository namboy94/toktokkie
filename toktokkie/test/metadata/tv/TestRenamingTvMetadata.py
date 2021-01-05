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
from toktokkie.metadata.enums import IdType
from toktokkie.Directory import Directory
from toktokkie.test.TestFramework import _TestFramework
from toktokkie.metadata.tv.Tv import Tv


class TestRenamingTvMetadata(_TestFramework):
    """
    Class that tests renaming the content of tv series metadata
    """

    def test_simple_renaming(self):
        """
        Tests renaming a simple tv series with a single season
        """
        otgw = self.get("Over the Garden Wall")
        otgw_dir = Directory(otgw)
        otgw_dir.rename(noconfirm=True)

        correct, wrong = self.scramble_episode_names(otgw)
        otgw_dir.rename(noconfirm=True)

        for _file in correct:
            self.assertTrue(os.path.isfile(_file))
        for _file in wrong:
            self.assertFalse(os.path.isfile(_file))

    def test_renaming_after_title_change(self):
        """
        Tests renaming after the title changed
        :return:
        """
        otgw = self.get("Over the Garden Wall")
        otgw_dir = Directory(otgw)

        otgw_dir.metadata.set_ids(IdType.ANILIST, ["19815"])
        otgw_dir.rename(noconfirm=True)

        self.assertEqual(otgw_dir.metadata.name, "No Game, No Life")
        self.assertTrue(otgw_dir.path.endswith("No Game, No Life"))
        self.assertTrue(
            otgw_dir.metadata.directory_path.endswith("No Game, No Life")
        )
        self.assertTrue(os.path.isfile(os.path.join(
            otgw_dir.path,
            "Season 1",
            "No Game, No Life - S01E01 - Chapter 1; The Old Grist Mill.mkv",
        )))

    def test_generic_renaming(self):
        """
        Tests renaming with unknown or missing IMDB IDs
        """
        otgw = self.get("Over the Garden Wall")
        otgw_dir = Directory(otgw)
        meta: Tv = otgw_dir.metadata

        sample = os.path.join(
            otgw, "Season 1/Over the Garden Wall - S01E02 - Episode 2.mkv"
        )
        self.assertFalse(os.path.isfile(sample))

        meta.ids = {IdType.IMDB: ["0"]}
        otgw_dir.rename(noconfirm=True)
        self.assertTrue(os.path.isfile(sample))

        meta.ids = {IdType.KITSU: ["0"]}
        otgw_dir.rename(noconfirm=True)
        self.assertTrue(os.path.isfile(sample))

        meta.ids = {}
        otgw_dir.rename(noconfirm=True)
        self.assertTrue(os.path.isfile(sample))

    def test_renaming_spinoff(self):
        """
        Tests if renaming works with a spinoff series
        """
        haruhi = self.get("The Melancholy of Haruhi Suzumiya")
        haruhi_dir = Directory(haruhi)

        correct, wrong = self.scramble_episode_names(haruhi)
        haruhi_dir.rename(noconfirm=True)

        for _file in correct:
            self.assertTrue(os.path.isfile(_file))
        for _file in wrong:
            self.assertFalse(os.path.isfile(_file))

    def test_renaming_multi_episodes(self):
        """
        Tests renaming series with multi episode directives
        :return: None
        """
        fullmetal = self.get("Fullmetal Alchemist")
        fullmetal_dir = Directory(fullmetal)
        meta: Tv = fullmetal_dir.metadata

        meta.add_multi_episode(IdType.IMDB, 1, 9, 10)
        fullmetal_dir.rename(noconfirm=True)

        self.assertTrue(os.path.isfile(os.path.join(
            fullmetal,
            "Season 1",
            "Fullmetal Alchemist - S01E09-E10 - "
            "Be Thou for the People ǁ The Phantom Thief.mp4",
        )))

    def test_renaming_excluded_episodes(self):
        """
        Tests renaming series with exclusion directives
        :return: None
        """
        fullmetal = self.get("Fullmetal Alchemist")
        fullmetal_dir = Directory(fullmetal)
        meta: Tv = fullmetal_dir.metadata

        excluded = os.path.join(
            fullmetal,
            "Season 1",
            "Fullmetal Alchemist - S01E05 - "
            "The Man with the Mechanical Arm.mp4",
        )
        self.assertTrue(os.path.isfile(excluded))

        meta.add_exclude(IdType.IMDB, 1, 5)
        fullmetal_dir.rename(noconfirm=True)

        self.assertFalse(os.path.isfile(excluded))

    def test_loading_episode_name_with_unimplemented_id_type(self):
        """
        Tests if a correct generic episode name is generated
        :return: None
        """
        result = Tv.load_episode_name("1", IdType.KITSU, 1, 1)
        self.assertEqual(result, "Episode 1")
