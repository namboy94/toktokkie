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

from toktokkie.verification.lib.anilist.Cache import Cache
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.EntriesInAnilistVerificator import \
    EntriesInAnilistVerificator


class TestEntriesInAnilistVerificator(TestVerificator):
    """
    Class that tests if the EntriesInAnilistVerificator
    works correctly
    """

    prepared_directories = ["Steins;Gate", "Kimi no Na wa. (2016)", "91 Days"]
    """
    Prepared metadata directories.
    """

    verification_attr = {"anilist_user": "namboy94"}
    """
    Verification attributes
    """

    verificator_cls = EntriesInAnilistVerificator
    """
    Verificator class to test
    """

    def setUp(self):
        """
        Creates easy to use instance variables for verificators
        :return: None
        """
        super().setUp()
        self.steinsgate, self.kiminonawa, self.days = [
            self.verificators["Steins;Gate"],
            self.verificators["Kimi no Na wa. (2016)"],
            self.verificators["91 Days"]
        ]  # type: EntriesInAnilistVerificator

    def test_all_entries_in_list(self):
        """
        Tests if the verificator correctly identifies all items being
        in the list
        :return: None
        """
        self.assertTrue(self.steinsgate.verify())
        self.assertTrue(self.kiminonawa.verify())

    def test_missing_anime_series_entries(self):
        """
        Tests if missing anime series entries are correctly identified
        :return: None
        """

        for season in self.steinsgate.directory.metadata.seasons.list:
            for mal_id in season.mal_ids.list:
                entry = self.steinsgate.handler.entries.pop(mal_id)
                self.assertFalse(self.steinsgate.verify())
                self.steinsgate.handler.entries[mal_id] = entry
                self.assertTrue(self.steinsgate.verify())

    def test_missing_anime_movie_entries(self):
        """
        Tests if missing anime movie entries are correctly identified
        :return: None
        """
        mal_id = self.kiminonawa.directory.metadata.mal_id
        entry = self.kiminonawa.handler.entries.pop(mal_id)
        self.assertFalse(self.kiminonawa.verify())
        self.kiminonawa.handler.entries[mal_id] = entry
        self.assertTrue(self.kiminonawa.verify())

    def test_fixing_anilist_entry(self):
        """
        Tests fixing an anilist entry
        :return: None
        """
        cacheget = Cache.get_handler_for_user

        y_count = {"count": 0}
        user_input = ["y", "n", "y", "n", "y", "stop"]

        def input_func(_: str) -> str:
            prompt = user_input.pop(0)
            if prompt == "y":
                y_count["count"] += 1
            self.assertNotEqual(prompt, "stop")

            if len(user_input) == 1:
                Cache.get_handler_for_user = cacheget

            return prompt

        mal_id = self.kiminonawa.directory.metadata.mal_id
        self.kiminonawa.handler.entries.pop(mal_id)

        try:
            Cache.get_handler_for_user = lambda x, y: self.kiminonawa.handler

            self.assertFalse(self.kiminonawa.verify())

            self.kiminonawa.input_function = input_func
            self.kiminonawa.fix()

            self.assertTrue(self.kiminonawa.verify())
            self.assertEqual(y_count["count"], 3)

        except (Exception, BaseException) as e:
            Cache.get_handler_for_user = cacheget
            raise e

    def test_fixing_all_anime_series_seasons(self):
        """
        Tests fixing all missing anilist entries of an anime series
        :return: None
        """
        for season in self.steinsgate.directory.metadata.seasons.list:
            for mal_id in season.mal_ids.list:
                self.steinsgate.handler.entries.pop(mal_id)

        self.assertFalse(self.steinsgate.verify())

        self.steinsgate.input_function = lambda x: "y"
        self.steinsgate.fix()

        self.assertTrue(self.steinsgate.verify())

    def test_handling_of_missing_anilist_id_for_mal_id(self):
        """
        Tests that the verificator works correctly for a mal ID
        that does not exist on anilist.co
        """
        self.assertTrue(self.days.verify())
