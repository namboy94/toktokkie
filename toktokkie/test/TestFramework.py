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


class TestFramework(unittest.TestCase):
    """
    A class that implements standard setUp and tearDown methods for unit tests
    """

    resources = "toktokkie/test/res"
    """
    The directory containing the original test resources.
    The contents of this directory should not be modified during tests.
    """

    test_res = "test-res"
    """
    The directory containing a fresh copy of the test resources.
    May be modified during tests. Regenerated in setUp method.
    """

    def cleanup(self):
        """
        Deletes any generates resources
        :return:
        """
        if os.path.exists(self.test_res):
            shutil.rmtree(self.test_res)

    def setUp(self):
        """
        Sets up the test resources
        :return: None
        """
        self.cleanup()
        try:
            shutil.copytree(self.resources, self.test_res)
        except FileNotFoundError:
            shutil.copytree(os.path.basename(self.resources), self.test_res)

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
        return os.path.join(self.test_res, directory)
