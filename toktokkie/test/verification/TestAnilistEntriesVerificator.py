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

from toktokkie.metadata.types.MetaType import Int
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.AnilistEntriesVerificator import \
    AnilistEntriesVerificator


class TestAnilistEntriesVerificator(TestVerificator):
    """
    Class that tests if the AnilistEntriesVerificator
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

    verificator_cls = AnilistEntriesVerificator
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
        ]  # type: AnilistEntriesVerificator
        # Preload cache
        self.anilist_api.get_anime_list(self.steinsgate.username)

    def test_all_entries_in_list(self):
        """
        Tests if the verificator correctly identifies all items being
        in the list
        :return: None
        """
        self.assertTrue(self.steinsgate.verify())
        self.assertTrue(self.kiminonawa.verify())

    def test_handling_of_missing_anilist_id_for_mal_id(self):
        """
        Tests that the verificator works correctly for a mal ID
        that does not exist on anilist.co
        """
        self.assertTrue(self.days.verify())

    def test_missing_anime_series_entries(self):
        """
        Tests if missing anime series entries in the list
        are correctly identified
        :return: None
        """
        self.assertTrue(self.steinsgate.verify())
        self.steinsgate.directory.metadata.seasons.list[0].mal_ids.append(
            Int(413)  # Mars of destruction
        )
        self.steinsgate.directory.write_metadata()
        self.assertFalse(self.steinsgate.verify())

    def test_missing_anime_movie_entries(self):
        """
        Tests if missing anime movie entries are correctly identified
        :return: None
        """
        self.assertTrue(self.kiminonawa.verify())
        self.kiminonawa.directory.metadata.mal_id = Int(413)
        self.kiminonawa.directory.write_metadata()
        self.assertFalse(self.kiminonawa.verify())
