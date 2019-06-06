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
from toktokkie.test.TestFramework import TestFramework


class TestCheck(TestFramework):
    """
    Class that checks whether or not the validity checks work as intended
    """

    config = {
        "tvdb_api": tvdb_api.Tvdb()
    }

    def verify(self, should_dir: str, is_dir: str):
        """
        Makes sure that two directories share the same content.
        :param should_dir: Directory
        :param is_dir:
        :return:
        """
        self.assertTrue(os.path.isdir(should_dir))
        self.assertTrue(os.path.isdir(is_dir))
        should_children = os.listdir(should_dir)
        is_children = os.listdir(is_dir)

        self.assertEqual(len(should_children), len(is_children))

        for child in should_children:
            self.assertTrue(child in is_children)
            child_path = os.path.join(should_dir, child)

            if os.path.isdir(child_path):
                self.verify(child_path, os.path.join(is_dir, child))

    def test_check(self):
        """

        :return: None
        """
        suzu = Directory(self.get("Suzumiya Haruhi no Yuuutsu"))
        self.assertTrue(suzu.check(False, False, self.config))
