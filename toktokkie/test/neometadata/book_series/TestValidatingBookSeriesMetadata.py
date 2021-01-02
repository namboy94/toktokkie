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

from jsonschema import validate, ValidationError
from toktokkie.neometadata.book_series.BookSeries import BookSeries
from toktokkie.test.TestFramework import _TestFramework


class TestValidatingBookSeriesMetadata(_TestFramework):
    """
    Class that tests the BookSeriesVaildator class
    """

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        valid_data = [
            {"type": "book_series", "ids": {"isbn": ["100"]}, "volumes": {}},
            {"type": "book_series", "ids": {"isbn": ["100"]}, "volumes": {
                "1": {"ids": {"isbn": ["1000"]}}
            }}
        ]
        invalid_data = [
            {},
            {"type": "book_series", "ids": {"isbn": 100}, "volumes": {}},
            {"type": "book_series", "volumes": {}},
            {"type": "book_series", "ids": {}},
            {"type": "movie", "ids": {"isbn": ["100"]}, "volumes": {}},
            {"type": "book_series", "ids": {"isbn": "100"}, "volumes": {}},
            {"type": "book_series", "ids": {"isbn": ["100"]}, "volumes": {
                "1": {"ids": {"isbn": 1000}}
            }},
            {"type": "book_series", "ids": {"isbn": ["100"]}, "volumes": {
                "ids": {"isbn": ["1000"]}
            }},
        ]
        schema = BookSeries.build_schema()
        for entry in valid_data:
            validate(entry, schema)
        for entry in invalid_data:
            try:
                validate(entry, schema)
                self.fail()
            except ValidationError:
                pass
