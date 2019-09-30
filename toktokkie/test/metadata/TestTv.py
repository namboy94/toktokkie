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
import tvdb_api
from toktokkie.Directory import Directory
from toktokkie.exceptions import InvalidMetadata
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.test.metadata.TestMetadata import _TestMetadata


class TestTv(_TestMetadata):
    """
    Test class for TV metadata
    """

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        got = Directory(self.get("Game of Thrones"))
        got.rename(noconfirm=True)

        for mode, data in {
            True: {
                "Season 1": [
                    "S01E01 - Winter Is Coming.txt",
                    "S01E03 - Lord Snow",
                    "S01E04 - Cripples, Bastards, and Broken Things.bin",
                    "S01E09-E10 - Baelor ǁ Fire and Blood.txt"
                ],
                "Season 2": [
                    "S02E03 - What is Dead May Never Die.txt"
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
                    print(episode)

                    episode_file = "test-res/{}/{}/{} - {}".format(
                        "Game of Thrones", season, got, episode
                    )
                    self.assertEqual(
                        mode,
                        os.path.isfile(episode_file)
                    )

        breaking_bad = "Breaking Bad/Breaking Bad - S01E01 - Pilot.txt"
        self.assertTrue(os.path.isfile(os.path.join(
            got.path, breaking_bad
        )))

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        pass

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        path = self.get("Suzumiya Haruhi no Yuuutsu")

        try:
            TvSeries(path, {})
            self.fail()
        except InvalidMetadata:
            pass

    def test_checking(self):
        """
        Tests if the checking mechanisms work correctly
        :return: None
        """
        suzu = Directory(self.get("Suzumiya Haruhi no Yuuutsu"))
        self.assertTrue(suzu.check(False, False, {
            "tvdb_api": tvdb_api.Tvdb()
        }))
