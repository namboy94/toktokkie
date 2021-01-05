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
from toktokkie.neometadata.enums import IdType
from toktokkie.Directory import Directory
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
        self.assertEqual(book_path, faust.book_path)
        self.assertTrue(os.path.isfile(book_path))
        os.rename(book_path, os.path.join(faust.directory_path, "x.epub"))
        self.assertFalse(os.path.isfile(book_path))
        faust.rename(noconfirm=True)
        self.assertTrue(os.path.isfile(book_path))

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        faust = self.get("Faust")
        correct = os.path.join(faust, "Faust.epub")
        incorrect = os.path.join(faust, "Fausti.epub")
        os.rename(correct, incorrect)

        self.assertFalse(os.path.isfile(correct))
        self.assertTrue(os.path.isfile(incorrect))

        faust_dir = Directory(faust)
        faust_dir.rename(noconfirm=True)

        self.assertTrue(os.path.isfile(correct))
        self.assertFalse(os.path.isfile(incorrect))

        faust_dir.metadata.set_ids(IdType.ANILIST, [39115])
        faust_dir.rename(noconfirm=True)

        self.assertEqual(faust_dir.metadata.name, "Spice & Wolf")
        self.assertFalse(os.path.isfile(correct))
        self.assertTrue(os.path.isfile(
            self.get("Spice & Wolf/Spice & Wolf.epub")
        ))
