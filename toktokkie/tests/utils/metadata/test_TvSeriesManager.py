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
import unittest
from toktokkie.utils.metadata.TVSeriesManager import TVSeriesManager
from toktokkie.tests.helpers import generate_test_directory, cleanup, test_dir


class TVSeriesManagerUnitTests(unittest.TestCase):

    def setUp(self):
        generate_test_directory()

    def tearDown(self):
        cleanup()

    def test_tv_series_directory_check(self):
        self.assertTrue(TVSeriesManager.is_tv_series_directory(os.path.join(test_dir, "Game of Thrones")))
        self.assertTrue(TVSeriesManager.is_tv_series_directory(os.path.join(test_dir, "The Big Bang Theory")))
        self.assertFalse(TVSeriesManager.is_tv_series_directory(os.path.join(test_dir, "NotAShow")))

    def test_recursive_tv_series_checker(self):
        directories = TVSeriesManager.find_recursive_tv_series_directories(test_dir)
        self.assertEqual(len(directories), 4)
        self.assertTrue(os.path.join(test_dir, "Game of Thrones") in directories)
        self.assertTrue(os.path.join(test_dir, "The Big Bang Theory") in directories)
        self.assertTrue(os.path.join(test_dir, "Re Zero") in directories)
        self.assertTrue(os.path.join(test_dir, "NotExistingShow") in directories)
        self.assertTrue(os.path.join(test_dir, "NotAShow") not in directories)
        self.assertTrue(os.path.join(test_dir, "OtherMedia") not in directories)

    def test_recursive_tv_series_checker_with_single_folder(self):
        directories = TVSeriesManager.find_recursive_tv_series_directories(os.path.join(test_dir, "Game of Thrones"))
        self.assertEqual(len(directories), 1)
        self.assertTrue(os.path.join(test_dir, "Game of Thrones") in directories)
        self.assertTrue(os.path.join(test_dir, "The Big Bang Theory") not in directories)
        self.assertTrue(os.path.join(test_dir, "Re Zero") not in directories)
        self.assertTrue(os.path.join(test_dir, "NotExistingShow") not in directories)
        self.assertTrue(os.path.join(test_dir, "NotAShow") not in directories)
        self.assertTrue(os.path.join(test_dir, "OtherMedia") not in directories)
