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
from toktokkie.Directory import Directory
from toktokkie.verification import get_verificators, all_verificators
from toktokkie.verification.AnilistEntriesVerificator import \
    AnilistEntriesVerificator
from toktokkie.verification.AnilistRelationVerificator import AnilistRelationVerificator
from toktokkie.verification.TVDBEpisodeCountVerificator import TVDBEpisodeCountVerificator
from toktokkie.verification.SeasonMetadataVerificator import SeasonMetadataVerificator
from toktokkie.verification.EpisodeNameVerificator import EpisodeNameVerificator
from toktokkie.verification.FolderIconVerificator import FolderIconVerificator
from toktokkie.test.verification.TestVerificator import TestVerificator


class TestVerificatorFetcher(TestVerificator):
    """
    Test class for the get_verificators method that makes it possible
    to get the correct verificators for any given metadata type
    """

    prepared_directories = ["Steins;Gate"]
    """
    A list of directories to prepare for testing
    """

    def test_fetching_verificators(self):
        """
        Tests fetching verificators
        :return: None
        """

        base, tv_series, anime_series, movie, anime_movie = \
            self.generate_sample_metadata()

        tested = {}
        for verificator in all_verificators:
            tested[verificator] = False

        for directory, expected in {
            base: [
                FolderIconVerificator
            ],
            tv_series: [
                FolderIconVerificator,
                SeasonMetadataVerificator,
                TVDBEpisodeCountVerificator,
                EpisodeNameVerificator
            ],
            anime_series: [
                FolderIconVerificator,
                SeasonMetadataVerificator,
                AnilistRelationVerificator,
                AnilistEntriesVerificator,
                TVDBEpisodeCountVerificator,
                EpisodeNameVerificator
            ],
            movie: [
                FolderIconVerificator
            ],
            anime_movie: [
                FolderIconVerificator,
                AnilistEntriesVerificator
            ]
        }.items():
            verificators = get_verificators(directory, {
                "anilist_user": "namboy94",
                "ignore_on_hold": True,
                "naming_scheme": "plex",
                "naming_agent": "tvdb"
            })
            verificator_types = list(map(lambda x: type(x), verificators))

            for verificator in expected:
                tested[verificator] = True
                print("-----------")
                print(verificator)
                print(expected)
                print(verificator_types)
                self.assertTrue(verificator in verificator_types)

            for verificator in all_verificators:
                if verificator not in expected:
                    self.assertFalse(verificator in verificator_types)

        for _, state in tested.items():
            self.assertTrue(state)

    def test_retrieving_verificator_with_missing_parameters(self):
        """
        Tests retrieving verificators without a required parameter
        :return: None
        """
        directory = Directory(os.path.join(self.testdir, "Steins;Gate"))
        verificators = get_verificators(directory, {})
        verificator_types = list(map(lambda x: type(x), verificators))

        self.assertTrue(FolderIconVerificator in verificator_types)
        self.assertFalse(EpisodeNameVerificator in verificator_types)
        self.assertFalse(AnilistEntriesVerificator in verificator_types)
