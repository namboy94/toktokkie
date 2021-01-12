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
from typing import List
from unittest.mock import patch
from toktokkie.metadata.book.Book import Book
from toktokkie.test.TestFramework import _TestFramework


class TestEditCommand(_TestFramework):
    """
    Class that tests the edit command
    """

    def test_printing_directory_info(self):
        """
        Tests printing directory info
        :return: None
        """
        history = []

        def call_dummy(args: List[str]):
            history.append(args)

        path = self.get("Faust")
        meta = Book(path)
        meta_path = meta.metadata_file

        with patch("toktokkie.commands.edit.call", call_dummy):
            os.environ["EDITOR"] = ""
            os.environ.pop("EDITOR")
            self.execute_command(["edit", path], [])
            self.assertEqual(history, [])

            self.execute_command(["edit", path, "--editor", "abc"], [])
            self.assertEqual(history, [["abc", meta_path]])

            os.environ["EDITOR"] = "xyz"
            self.execute_command(["edit", path], [])
            self.assertEqual(history, [["abc", meta_path], ["xyz", meta_path]])
