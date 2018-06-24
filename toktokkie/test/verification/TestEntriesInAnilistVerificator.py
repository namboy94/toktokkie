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
import shutil
from toktokkie.Directory import Directory
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.test.resources import get_metadata_paths
from toktokkie.verification.EntriesInAnilistVerificator import \
    EntriesInAnilistVerificator


class TestEntriesInAnilistVerificator(TestVerificator):
    """
    Class that tests if the EntriesInAnilistVerificator
    works correctly
    """

    def setUp(self):
        """
        Copies some valid metadata directories into the testing directory
        :return: None
        """
        super().setUp()
        metadatas = get_metadata_paths()
        print(metadatas)
        for item in ["Steins;Gate", "Kimi no Na wa. (2016)"]:
            shutil.copytree(metadatas[item], os.path.join(self.testdir, item))
        self.steinsgate = EntriesInAnilistVerificator(
            Directory(os.path.join(self.testdir, "Steins;Gate")),
            {"anilist_user": "namboy94"}
        )
        self.kiminonawa = EntriesInAnilistVerificator(
            Directory(os.path.join(self.testdir, "Kimi no Na wa. (2016)")),
            {"anilist_user": "namboy94"}
        )

    def test_all_entries_in_list(self):
        """
        Tests if the verificator correctly identifies all items being
        in the list
        :return: None
        """
        self.assertTrue(self.steinsgate.verify())
        self.assertTrue(self.kiminonawa.verify())
