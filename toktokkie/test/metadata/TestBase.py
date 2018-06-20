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
from toktokkie.test.metadata.MetadataTester import MetadataTester
from toktokkie.metadata.Base import Base
from toktokkie.metadata.TvSeries import TvSeries


class TestBase(MetadataTester):
    """
    Class that contains tests for the Base Metadata class
    """

    def test_generating_and_reading_base_metadata(self):
        """
        Tests generating and reading a Base metadata object
        :return: None
        """
        metadata = self.generate_metadata(["TestName", "Tag1,Tag2"])

        self.assertEqual(metadata.type.to_json(), "base")
        self.assertEqual(metadata.name.to_json(), "TestName")
        self.assertEqual(metadata.tags.to_json(), ["Tag1", "Tag2"])

        self.verify_metadata(
            {"type": "base", "name": "TestName", "tags": ["Tag1", "Tag2"]},
            metadata
        )

        metadata.write(self.testjson)
        written = Base.from_json_file(self.testjson)

        self.assertEqual(metadata.to_json(), written.to_json())
        self.assertTrue(os.path.isfile(self.testjson))

    def test_subclass_check(self):
        """
        Tests if the is_subclass method works correctly
        :return: None
        """
        self.assertTrue(Base.is_subclass_of(object))
        self.assertFalse(Base.is_subclass_of(str))
        self.assertFalse(Base.is_subclass_of(TvSeries))
