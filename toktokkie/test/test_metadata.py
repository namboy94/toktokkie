"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

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
"""

import os
import shutil
import unittest
from unittest import mock
from toktokkie.metadata.Base import Base


class MetadataUnitTests(unittest.TestCase):
    """
    Unit tests for the metadata
    """

    testdir = "testdir"
    testjson = os.path.join(testdir, "test.json")

    def setUp(self):
        """
        Creates the test directory after deleting any previously existing ones
        :return: None
        """
        self.tearDown()
        os.makedirs("testdir")

    def tearDown(self):
        """
        Deletes all test directories
        :return: None
        """
        if os.path.isdir("testdir"):
            shutil.rmtree("testdir")

    def test_defaults_base_metadata(self):
        """
        Tests the metadata generation of the Base class when providing
        default values
        :return: None
        """
        with mock.patch("builtins.input", return_value=""):
            metadata = Base.generate_from_prompts(self.testdir)

        self.assertEquals(
            metadata.to_json(),
            {"type": "base", "name": "testdir", "tags": []}
        )

    def test_generating_and_reading_base_metadata(self):
        """
        Tests generating and reading a Base metadata object
        :return: None
        """
        user_input = ["TestName", "Tag1,Tag2"]
        with mock.patch("builtins.input", side_effect=user_input):
            metadata = Base.generate_from_prompts(self.testdir)

        self.assertEquals(metadata.type.to_json(), "base")
        self.assertEquals(metadata.name.to_json(), "TestName")
        self.assertEquals(metadata.tags.to_json(), ["Tag1", "Tag2"])

        self.assertEquals(metadata.to_json(), {
            "type": "base", "name": "TestName", "tags": ["Tag1", "Tag2"]
        })
        metadata.write(self.testjson)
        written = Base.from_json_file(self.testjson)

        self.assertEquals(metadata.to_json(), written.to_json())
        self.assertTrue(os.path.isfile(self.testjson))

    def test_generating_and_reading_tv_series_metadata(self):
        """
        Tests generating and readin a TvSeries Metadata object
        :return: None
        """
        user_input = []
