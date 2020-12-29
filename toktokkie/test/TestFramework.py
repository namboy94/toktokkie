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


class _TestFramework(unittest.TestCase):
    """
    A class that implements standard setUp and tearDown methods for unit tests
    """

    resources = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "res"
    )
    """
    The directory containing the original test resources.
    The contents of this directory should not be modified during tests.
    """

    res_dir = "/tmp/toktokkie-test-res"
    """
    The directory containing a fresh copy of the test resources.
    May be modified during tests. Regenerated in setUp method.
    """

    def cleanup(self):
        """
        Deletes any generated resources
        :return:
        """
        if os.path.exists(self.res_dir):
            shutil.rmtree(self.res_dir)

    def setUp(self):
        """
        Sets up the test resources
        :return: None
        """
        self.cleanup()
        try:
            shutil.copytree(self.resources, self.res_dir)
        except FileNotFoundError:
            shutil.copytree(os.path.basename(self.resources), self.res_dir)

    def tearDown(self):
        """
        Deletes the test resources
        :return: None
        """
        self.cleanup()

    def get(self, directory: str) -> str:
        """
        Retrieves the path to a test resource
        :param directory: The directory to get
        :return: The path to the directory
        """
        return os.path.join(self.res_dir, directory)

    def assert_directories_same(self, should_dir: str, is_dir: str):
        """
        Makes sure that two directories share the same content.
        :param should_dir: The first directory
        :param is_dir: The second directory
        :return: None
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
                self.assert_directories_same(
                    child_path, os.path.join(is_dir, child)
                )
