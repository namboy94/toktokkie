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
from unittest import TestCase


class TestVerificator(TestCase):
    """
    Test class for a verificator. Also defines common methods for all
    other verificator tests
    """

    testdir = "testdir"
    """
    Directory in which to store any generated files
    """

    def setUp(self):
        """
        Creates the test directory after deleting any previously existing ones
        :return: None
        """
        self.cleanup()
        os.makedirs(self.testdir)

    def tearDown(self):
        """
        Deletes all test directories
        :return: None
        """
        self.cleanup()

    def cleanup(self):
        """
        Cleans up files and directories generated while testing
        :return: None
        """
        if os.path.isdir(self.testdir):
            shutil.rmtree(self.testdir)
