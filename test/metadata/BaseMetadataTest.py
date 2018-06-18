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
from test.metadata.MetadataTester import MetadataTester
from toktokkie.metadata.Base import Base


class BaseMetadataTest(MetadataTester):
    """
    Class that contains tests for the Base Metadata class
    """

    def test_generating_and_reading_base_metadata(self):
        """
        Tests generating and reading a Base metadata object
        :return: None
        """
        metadata = self.execute_with_mocked_input(
            ["TestName", "Tag1,Tag2"],
            lambda: Base.generate_from_prompts(self.testdir)
        )  # type: Base

        self.assertEqual(metadata.type.to_json(), "base")
        self.assertEqual(metadata.name.to_json(), "TestName")
        self.assertEqual(metadata.tags.to_json(), ["Tag1", "Tag2"])

        self.assertEqual(metadata.to_json(), {
            "type": "base", "name": "TestName", "tags": ["Tag1", "Tag2"]
        })
        metadata.write(self.testjson)
        written = Base.from_json_file(self.testjson)

        self.assertEqual(metadata.to_json(), written.to_json())
        self.assertTrue(os.path.isfile(self.testjson))
