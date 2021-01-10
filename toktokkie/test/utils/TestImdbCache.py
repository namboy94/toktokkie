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

import time
from unittest.mock import patch
from toktokkie.utils.ImdbCache import ImdbCache
from toktokkie.test.TestFramework import _TestFramework


class TestImdbCache(_TestFramework):
    """
    Tests for the ImdbCache class
    """

    def test_caching(self):
        """
        Tests if the caching forks correctly
        :return: None
        """
        start = time.time()
        to_mock = "toktokkie.utils.ImdbCache.ImdbCache.imdb_api" \
                  ".get_movie_episodes"

        episode_one = ImdbCache.load_episode_name("tt0944947", 1, 1)

        mid = time.time()
        with patch(to_mock, lambda x: 1 / 0):
            episode_one_cached = ImdbCache.load_episode_name("tt0944947", 1, 1)
            episode_two_cached = ImdbCache.load_episode_name("tt0944947", 1, 2)
            out_of_range = ImdbCache.load_episode_name("tt0944947", 1, 100)

            try:
                ImdbCache.load_episode_name("tt0903747", 1, 1)
                self.fail()
            except ZeroDivisionError:
                pass

        end = time.time()

        self.assertEqual(episode_one, "Winter Is Coming")
        self.assertEqual(episode_one_cached, "Winter Is Coming")
        self.assertEqual(episode_two_cached, "The Kingsroad")
        self.assertEqual(out_of_range, "Episode 100")

        non_cached = mid - start
        cached = end - mid

        self.assertTrue(cached < non_cached)
        self.assertTrue("0944947" in ImdbCache.episode_cache)
        self.assertEqual(
            ImdbCache.episode_cache["0944947"][1][1]["title"],
            "Winter Is Coming"
        )

    def test_invalid_id(self):
        """
        Tests using an invalid ID
        :return: None
        """
        self.assertEqual("Episode 1", ImdbCache.load_episode_name("12", 1, 1))

    def test_out_of_range_episode(self):
        """
        Tests using out of range episodes/seasons
        :return: None
        """
        self.assertEqual(
            "Episode 100",
            ImdbCache.load_episode_name("tt0903747", 1, 100)
        )
        self.assertEqual(
            "Episode 1",
            ImdbCache.load_episode_name("tt0903747", 10, 1)
        )

    def test_special_season(self):
        """
        Tests fetching data from special season
        :return: None
        """
        self.assertEqual(
            "Episode 1",
            ImdbCache.load_episode_name("tt5607616", 0, 1)
        )
        # TODO figure out a better way to include special seasons
