"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

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
LICENSE
"""

# imports
import os
import shutil
import unittest
from toktokkie.utils.iconizing.Iconizer import Iconizer


class IconizerUnitTests(unittest.TestCase):

    def setUp(self):
        shutil.copytree(os.path.join("toktokkie", "tests", "resources", "directories"), "temp_testing")
        self.game_of_thrones = os.path.join("temp_testing", "Game of Thrones")
        self.native_iconizer = Iconizer()

    def tearDown(self):
        self.native_iconizer.reverse_iconization("temp_testing")
        shutil.rmtree("temp_testing")

    def test_native_iconizing(self):

        if self.native_iconizer.procedure is not None:
            self.assertEqual(self.native_iconizer.procedure.get_icon_file(self.game_of_thrones), None)

            self.native_iconizer.recursive_iconize("temp_testing")

            self.assertNotEqual(self.native_iconizer.procedure.get_icon_file(self.game_of_thrones), None)
            self.assertTrue(self.native_iconizer.procedure.get_icon_file(self.game_of_thrones) in
                            [os.path.join(self.game_of_thrones, ".meta", "icons", "main.png"),
                             os.path.join(self.game_of_thrones, ".meta", "icons", "main.ico")])

            self.native_iconizer.reverse_iconization("temp_testing")

            if self.native_iconizer.procedure is not None:
                self.assertEqual(self.native_iconizer.procedure.get_icon_file(self.game_of_thrones), None)

    # noinspection PyMethodMayBeStatic
    def test_no_iconizer_available(self):

        iconizer = Iconizer()
        iconizer.procedure = None
        iconizer.recursive_iconize("temp_testing")  # Just to check that no errors are thrown
