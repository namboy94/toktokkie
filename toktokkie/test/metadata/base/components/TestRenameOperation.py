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
from colorama import Fore
from toktokkie.metadata.base.components.RenameOperation import RenameOperation
from toktokkie.test.TestFramework import _TestFramework


class TestRenameOperation(_TestFramework):
    """
    Class that tests the RenameOperation class
    """

    def test_sanitization_trimming(self):
        """
        Tests the filename sanitizer function's trimming functionality
        :return: None
        """
        parent = self.get("Fureraba")
        sanitized = RenameOperation.sanitize(parent, "H" * 500)
        self.assertLess(len(os.path.basename(sanitized)), 250)

    def test_string_representation(self):
        """
        Tests the string representation of a renaming operation
        :return: None
        """
        operation = RenameOperation(self.get("Fureraba"), "New")
        self.assertTrue(Fore.LIGHTYELLOW_EX in str(operation))
        operation = RenameOperation(self.get("Fureraba"), "Fureraba")
        self.assertFalse(Fore.LIGHTYELLOW_EX in str(operation))
