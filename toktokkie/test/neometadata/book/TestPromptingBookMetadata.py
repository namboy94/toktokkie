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
from puffotter.os import touch
from unittest.mock import patch
from toktokkie.exceptions import InvalidDirectoryState
from toktokkie.neometadata.enums import IdType
from toktokkie.neometadata.book.Book import Book
from toktokkie.test.TestFramework import _TestFramework


class TestPromptingBookMetadata(_TestFramework):
    """
    Class that tests the BookPrompter class
    """

    def test_generating_new_book(self):
        """
        Tests prompting for new book metadata
        :return: None
        """
        path = self.get("McBeth")
        os.makedirs(path)
        with open(os.path.join(path, "McBeth.epub"), "w") as f:
            f.write("")

        with patch("builtins.input", side_effect=[
            "",  # tags
            "123",  # ISBN ID
            "", "", "",  # Other IDs
        ]):
            metadata = Book.from_prompt(path)
            metadata.write()

        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata.name, "McBeth")
        self.assertEqual(metadata.ids[IdType.ISBN], ["123"])

    def test_prompting_with_missing_book_file(self):
        """
        Tests if a missing book file is handled correctly while prompting
        :return: None
        """
        path = self.get("McBeth")
        os.makedirs(path)

        try:
            Book.from_prompt(path)
            self.fail()
        except InvalidDirectoryState as e:
            self.assertEqual(str(e), "No book file")

    def test_prompting_with_multiple_book_files(self):
        """
        Tests if a missing book file is handled correctly while prompting
        :return: None
        """
        path = self.get("McBeth")
        os.makedirs(path)
        touch(os.path.join(path, "Part 1.epub"))
        touch(os.path.join(path, "Part 2.epub"))
        print(os.listdir(path))

        try:
            Book.from_prompt(path)
            self.fail()
        except InvalidDirectoryState as e:
            self.assertEqual(str(e), "More than one book file")
