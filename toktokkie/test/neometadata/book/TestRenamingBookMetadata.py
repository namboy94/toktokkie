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
from toktokkie.neometadata.book.Book import Book
from toktokkie.test.TestFramework import _TestFramework


class TestRenamingBookMetadata(_TestFramework):
    """
    Class that tests the BookRenamer class
    """

    def test_book_renaming(self):
        """
        Tests renaming book directories
        :return: None
        """
        faust = Book(self.get("Faust"))
        book_path = os.path.join(faust.directory_path, "Faust.epub")
        self.assertTrue(os.path.isfile(book_path))
        os.rename(book_path, os.path.join(faust.directory_path, "x.epub"))
        self.assertFalse(os.path.isfile(book_path))
        faust.rename(noconfirm=True)
        self.assertTrue(os.path.isfile(book_path))
