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
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.EpisodeNameVerificator import \
    EpisodeNameVerificator


class TestEpisodeNameVerificator(TestVerificator):
    """
    Class that tests the Episode Name Verificator
    """

    media_dir = "Game of Thrones"
    """
    The directory in which to store the test media directory
    """

    verificator_cls = EpisodeNameVerificator
    """
    The Verificator class to test
    """

    structure = {
        media_dir: {
            "Season 1": [
                "Game of Thrones - S01E01 - Winter Is Coming.txt",
                "Game of Thrones - S01E02 - The Kingsroad.txt",
                "Game of Thrones - S01E03 - Lord Snow.txt"
            ],
            "Season 2": [
                "Game of Thrones - S02E01 - The North Remembers.txt",
                "Game of Thrones - S02E02 - The Night Lands.txt"
            ]
        }
    }
    """
    The test directory structure
    """

    metadatas = {
        media_dir: TvSeries({
            "type": "tv_series",
            "name": "Game of Thrones",
            "tags": [],
            "seasons": [
                {
                    "path": "Season 1",
                    "name": "Season 1",
                    "tvdb_ids": [121361],
                    "audio_langs": ["eng"],
                    "subtitle_langs": [],
                    "resolutions": [{"x": 1920, "y": 1080}]
                },
                {
                    "path": "Season 2",
                    "name": "Season 2",
                    "tvdb_ids": [121361],
                    "audio_langs": ["eng"],
                    "subtitle_langs": [],
                    "resolutions": [{"x": 1920, "y": 1080}]
                }
            ],
            "tvdb_excludes": [],
            "tvdb_irregular_season_starts": [],
            "tvdb_multi_episodes": []
        })
    }
    """
    The metadata for the media directories
    """

    verification_attr = {
        "naming_scheme": "plex",
        "naming_agent": "tvdb"
    }
    """
    Verification attributes
    """

    def test_valid_episodes(self):
        """
        Makes sure that the validator does not fire off false negatives
        :return: None
        """
        self.assertTrue(self.verificators[self.media_dir].verify())

    def test_invalid_episodes(self):
        """
        Makes sure that incorrect episode names are identified correctly
        :return: None
        """
        verificator = \
            self.verificators[self.media_dir]  # type: EpisodeNameVerificator

        for season_num, season in enumerate(["Season 1", "Season 2"]):
            season_path = os.path.join(self.testdir, self.media_dir, season)
            for episode_num, episode in enumerate(os.listdir(season_path)):
                episode_path = os.path.join(season_path, episode)
                new_episode = os.path.join(
                    season_path,
                    "Game of Thrones - S0" + str(season_num) +
                    "E0" + str(episode_num) + " - Random Name.txt"
                )
                os.rename(episode_path, new_episode)
                self.assertFalse(verificator.verify())
                self.setUp()

    def test_fixing(self):
        """
        Tests if fixing the episodes works correctly
        :return: None
        """
        verificator = \
            self.verificators[self.media_dir]  # type: EpisodeNameVerificator

        epi_one = os.path.join(
            self.testdir, self.media_dir, "Season 1",
            "Game of Thrones - S01E01 - Winter Is Coming.txt"
        )
        epi_two = os.path.join(
            self.testdir, self.media_dir, "Season 2",
            "Game of Thrones - S02E01 - The North Remembers.txt"
        )
        os.rename(
            epi_one,
            epi_one.replace("Winter Is Coming", "Summer is Going")
        )
        os.rename(
            epi_two,
            epi_two.replace("The North Remembers", "The South Forgets")
        )

        self.assertFalse(verificator.verify())
        self.assertFalse(os.path.exists(epi_one))
        self.assertFalse(os.path.isfile(epi_two))

        self.execute_with_mocked_input(
            ["y"],
            lambda: verificator.fix()
        )
        self.assertTrue(verificator.verify())
        self.assertTrue(os.path.isfile(epi_one))
        self.assertTrue(os.path.isfile(epi_two))
