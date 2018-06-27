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
from toktokkie.metadata.types.SeasonEpisode import SeasonEpisode
from toktokkie.metadata.types.EpisodeRange import EpisodeRange
from toktokkie.renaming.helper.resolve import get_episode_files
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.TVDBEpisodeCountVerificator import \
    TVDBEpisodeCountVerificator


class TestTVDBEpisodeCountVerificator(TestVerificator):
    """
    Class that tests the TVDB Episode Count Verificator
    """

    verificator_cls = TVDBEpisodeCountVerificator
    """
    The Verificator class to test
    """

    prepared_directories = ["Steins;Gate"]
    """
    Prepared media directories
    """

    def test_valid(self):
        """
        Makes sure that valid media is identified as such
        :return: None
        """
        verificator = self.verificators[
            "Steins;Gate"
        ]  # type: TVDBEpisodeCountVerificator
        self.assertTrue(verificator.verify())

    def test_with_missing_episode_files(self):
        """
        Makes sure that missing episode files are correctly identified
        :return: None
        """
        verificator = self.verificators[
            "Steins;Gate"
        ]  # type: TVDBEpisodeCountVerificator
        for season in verificator.directory.metadata.seasons.list:
            season_path = \
                os.path.join(self.testdir, "Steins;Gate", season.path)
            for episode in get_episode_files(season_path):
                os.remove(episode)
                self.assertFalse(verificator.verify())
                self.setUp()
                self.assertTrue(verificator.verify())

    def test_with_excluded_and_multi_episode(self):
        """
        Tests if excluded episodes and multi-episodes are correctly checked
        """
        verificator = self.verificators[
            "Steins;Gate"
        ]  # type: TVDBEpisodeCountVerificator
        season_one = list(filter(
            lambda x: x.path == "Season 1",
            verificator.directory.metadata.seasons.list
        ))[0]
        season_path = \
            os.path.join(self.testdir, "Steins;Gate", season_one.path)

        episodes = sorted(get_episode_files(season_path))

        # Excluded
        os.remove(episodes[0])
        self.assertFalse(verificator.verify())
        verificator.directory.metadata.tvdb_excludes.append(
            SeasonEpisode(1, 1)
        )
        self.assertTrue(verificator.verify())

        # Multi-Episodes
        os.remove(episodes[2])
        self.assertFalse(verificator.verify())
        verificator.directory.metadata.tvdb_multi_episodes.append(
            EpisodeRange(SeasonEpisode(1, 2), SeasonEpisode(1, 3))
        )
        self.assertTrue(verificator.verify())


    def test_fixing(self):
        """
        Tests fixing the incorrect amount of tvdb episode files
        :return: None
        """
        verificator = self.verificators[
            "Steins;Gate"
        ]  # type: TVDBEpisodeCountVerificator
        season_path = os.path.join(
            self.testdir,
            "Steins;Gate",
            verificator.directory.metadata.seasons.list[0].path
        )
        episode_file = os.path.join(
            season_path, os.listdir(season_path)[0]
        )

        os.remove(episode_file)
        self.assertFalse(verificator.verify())

        user_input = ["n", "y", "n", "y", "stop"]

        def input_func(_: str):
            prompt = user_input.pop(0)
            self.assertNotEqual("stop", prompt)
            if len(user_input) == 1:
                open(episode_file, "w").close()
            return prompt

        verificator.input_function = input_func
        verificator.fix()
        self.assertTrue(verificator.verify())
