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

from unittest.mock import patch
from toktokkie.test.TestFramework import _TestFramework


class TestPrintCommand(_TestFramework):
    """
    Class that tests the print command
    """

    def test_printing_directory_info(self):
        """
        Tests printing directory info
        :return: None
        """
        def print_dummy(string: str):
            self.assertTrue("book" in str(string))
            _ = 1 / 0

        path = self.get("Faust")
        with patch("builtins.print", print_dummy):
            try:
                self.execute_command(["print", path], [])
                self.fail()
            except ZeroDivisionError:
                pass
