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

from toktokkie.exceptions import InvalidMetadata
from toktokkie.neometadata.enums import IdType
from toktokkie.neometadata.book_series.components.BookVolume import BookVolume
from toktokkie.test.TestFramework import _TestFramework


class TestBookVolume(_TestFramework):
    """
    Class that tests the BookVolume component class
    """

    def test_initialization(self):
        """
        Tests the initialization of the component
        :return: None
        """
        volume = BookVolume(
            1,
            "/tmp/Name.epub",
            {IdType.ISBN: ["ABC"]},
            {IdType.ANILIST: ["XYZ"]}
        )
        self.assertEqual(volume.name, "Name")
        self.assertEqual(volume.path, "/tmp/Name.epub")

        self.assertEqual(
            volume.ids,
            {IdType.ANILIST: ["XYZ"], IdType.ISBN: ["ABC"]}
        )
        self.assertEqual(
            volume.json,
            {"ids": {IdType.ANILIST.value: ["XYZ"]}}
        )

    def test_missing_attributes(self):
        """
        Tests if missing attributes are handled correctly
        :return: None
        """
        try:
            BookVolume.from_json(1, "1", {}, {})
            self.fail()
        except InvalidMetadata:
            pass
