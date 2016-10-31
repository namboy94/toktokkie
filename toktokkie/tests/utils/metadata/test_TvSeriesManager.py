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
from toktokkie.utils.metadata.TVSeriesManager import TVSeriesManager


class TVSeriesManagerUnitTests(unittest.TestCase):

    def setUp(self):
        shutil.copytree("toktokkie/tests/resources/directories", "temp_testing")

    def tearDown(self):
        shutil.rmtree("temp_testing")

    def test_tv_series_directory_check(self):
        self.assertTrue(TVSeriesManager.is_tv_series_directory(os.path.join("temp_testing", "Game of Thrones")))
        self.assertTrue(TVSeriesManager.is_tv_series_directory(os.path.join("temp_testing", "The Big Bang Theory")))
        self.assertFalse(TVSeriesManager.is_tv_series_directory(os.path.join("temp_testing", "NotAShow")))

    def test_recursive_tv_series_checker(self):
        directories = TVSeriesManager.find_recursive_tv_series_directories("temp_testing")
        self.assertEqual(len(directories), 4)
        self.assertTrue(os.path.join("temp_testing", "Game of Thrones") in directories)
        self.assertTrue(os.path.join("temp_testing", "The Big Bang Theory") in directories)
        self.assertTrue(os.path.join("temp_testing", "Re Zero") in directories)
        self.assertTrue(os.path.join("temp_testing", "NotExistingShow") in directories)
        self.assertTrue(os.path.join("temp_testing", "NotAShow") not in directories)
        self.assertTrue(os.path.join("temp_testing", "OtherMedia") not in directories)

    def test_recursive_tv_series_checker_with_single_folder(self):
        directories = TVSeriesManager.find_recursive_tv_series_directories(os.path.join("temp_testing",
                                                                                        "Game of Thrones"))
        self.assertEqual(len(directories), 1)
        self.assertTrue(os.path.join("temp_testing", "Game of Thrones") in directories)
        self.assertTrue(os.path.join("temp_testing", "The Big Bang Theory") not in directories)
        self.assertTrue(os.path.join("temp_testing", "Re Zero") not in directories)
        self.assertTrue(os.path.join("temp_testing", "NotExistingShow") not in directories)
        self.assertTrue(os.path.join("temp_testing", "NotAShow") not in directories)
        self.assertTrue(os.path.join("temp_testing", "OtherMedia") not in directories)
