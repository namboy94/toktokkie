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
from jsonschema import validate, ValidationError
from toktokkie.exceptions import InvalidMetadata
from toktokkie.neometadata.book.Book import Book
from toktokkie.test.TestFramework import _TestFramework


class TestValidatingBookMetadata(_TestFramework):
    """
    Class that tests the BookVaildator class
    """

    def test_validating_missing_book_file(self):
        """
        Tests if a missing book file is handled correctly
        :return: None
        """
        faust = self.get("Faust")
        os.remove(os.path.join(faust, "Faust.epub"))
        try:
            Book(faust)
            self.fail()
        except InvalidMetadata:
            pass

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        schema = Book.build_schema()
        valid_data = [
            {"type": "book", "ids": {"isbn": ["100"]}}
        ]
        invalid_data = [
            {},  # Missing type and ids
            {"type": "book"},  # Missing ids
            {"type": "book", "ids": {}},  # 0 IDs
            {"type": "book", "ids": {"isbn": "100"}},  # Ids not a list
            {"type": "book", "ids": {"isbn": 100}},  # Ids not a list
            {"type": "book", "ids": {"isbn": [100]}},  # Ids not string
            {"type": "movie", "ids": {"isbn": ["100"]}}  # Wrong media type
        ]

        for entry in valid_data:
            validate(entry, schema)
        for entry in invalid_data:
            try:
                validate(entry, schema)
                self.fail()
            except ValidationError:
                pass
