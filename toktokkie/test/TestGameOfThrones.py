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
import unittest
from toktokkie.Directory import Directory


class TestGameOfThrones(unittest.TestCase):

    def cleanup(self):
        if os.path.exists("test-res"):
            shutil.rmtree("test-res")

    def setUp(self):
        self.cleanup()
        try:
            shutil.copytree("toktokkie/test/res", "test-res")
        except FileNotFoundError:
            shutil.copytree("res", "test-res")

    def tearDown(self):
        pass
        # self.cleanup()

    def test_renaming(self):
        directory = Directory("test-res/Game of Thrones")
        directory.rename()
