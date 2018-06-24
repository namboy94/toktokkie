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

from unittest import TestCase
from toktokkie.verification.lib.anilist.Cache import Cache
from toktokkie.verification.lib.anilist.enums import WatchingState, AiringState
from toktokkie.verification.lib.anilist.AnilistHandler import AnilistHandler


class TestAnilistApi(TestCase):
    """
    Class that tests the ani
    """

    def setUp(self):
        """
        Initializes an anilist handler
        :return: None
        """
        self.anilist_user = "namboy94"
        self.handler = Cache.get_handler_for_user(self.anilist_user)

    def test_fetching_anime_list(self):
        """
        Tests fetching the initial list
        :return: None
        """
        handler = AnilistHandler(self.anilist_user)
        self.assertGreater(len(handler.entries), 0)

    def test_individual_entry(self):
        """
        Tests the values of an individual entry
        :return: None
        """
        steinsgate = self.handler.entries[9253]  # El Psy Kongroo!
        self.assertEqual(steinsgate.mal_id, 9253)
        self.assertEqual(steinsgate.score, 10.0)  # It's so cool!
        self.assertEqual(steinsgate.progress, steinsgate.episodes)
        self.assertEqual(steinsgate.watching_status, WatchingState.COMPLETED)
        self.assertEqual(steinsgate.airing_status, AiringState.FINISHED)
        self.assertTrue(steinsgate.start_date.valid())
        self.assertTrue(steinsgate.completion_date.valid())

        for relation in steinsgate.relations:
            if relation.mal_id in [32188, 30484]:  # Steins;Gate 0
                self.assertFalse(relation.is_important())
            elif relation.mal_id in [17517]:  # Manga
                self.assertFalse(relation.is_important())
            else:
                self.assertTrue(relation.is_important())

    def test_cache(self):
        """
        Tests if the caching functionality is working correctly
        :return: None
        """

        original = Cache.get_handler_for_user(self.anilist_user)
        cached = Cache.get_handler_for_user(self.anilist_user)

        self.assertEqual(original, cached)

        new = Cache.get_handler_for_user(self.anilist_user, True)

        self.assertNotEqual(original, new)

    def test_fetching_anilist_id(self):
        """
        Tests fetching the anilist ID of a myanimelist ID
        :return: None
        """
        self.assertEqual(1, self.handler.get_anilist_id(1))  # Cowboy Bebop
        self.assertEqual(21127, self.handler.get_anilist_id(30484))  # S;G 0
        self.assertEqual(None, self.handler.get_anilist_id(36501))  # MahoYome0
