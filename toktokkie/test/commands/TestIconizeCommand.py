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
from toktokkie.metadata.book.Book import Book
from toktokkie.test.TestFramework import _TestFramework
from toktokkie.test.utils.iconizing.TestIconizer import DummyProcedure


class TestIconizerCommand(_TestFramework):
    """
    Class that tests the iconize command
    """

    def cleanup(self):
        """
        Resets the DummyProcedure
        :return: None
        """
        super().cleanup()
        DummyProcedure.history = []

    def test_iconizing(self):
        """
        Tests printing directory info
        :return: None
        """
        meta = Book(self.get("Faust"))
        with patch("toktokkie.utils.iconizing.Iconizer"
                   ".Iconizer.all_procedures", [DummyProcedure]):
            self.execute_command(["iconize", meta.directory_path], [])
        self.assertEqual(len(DummyProcedure.history), 1)
        self.assertEqual(DummyProcedure.history, [(
            meta.directory_path, meta.get_icon_file("main")
        )])
