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
import shutil
from typing import List, Any, Callable, Dict
from unittest import TestCase, mock
from toktokkie.metadata.Base import Base
from toktokkie.verfication.Verificator import Verificator
from toktokkie.exceptions import InvalidMetadataException, MetadataMismatch


class MetadataTester(TestCase):
    """
    Test framework for metadata classes
    """

    testdir = "testdir"
    """
    The directory with which to test the metadata class
    """

    testjson = os.path.join(testdir, "test.json")
    """
    The path to the metadata JSON file
    """

    metadata_cls = Base
    """
    The metadata class to test. Used by helper methods defined here
    """

    json_data_example = {
        "type": "base",
        "name": "TestName",
        "tags": ["Tag1", "Tag2"]
    }
    """
    An example metadata dictionary. Used to test generating the metadata
    object using a constructor call
    """

    def setUp(self):
        """
        Creates the test directory after deleting any previously existing ones
        :return: None
        """
        self.cleanup()
        os.makedirs(self.testdir)

    def tearDown(self):
        """
        Deletes all test directories
        :return: None
        """
        self.cleanup()

    def cleanup(self):
        """
        Cleans up files and directories generated while testing
        :return: None
        """
        if os.path.isdir(self.testdir):
            shutil.rmtree(self.testdir)

    @staticmethod
    def execute_with_mocked_input(
            prompt_input: List[str], action: Callable
    ) -> Any:
        """
        Executes a function with mocked user input
        :param prompt_input: The user input to mock
        :param action: The function to execute
        :return: The return value of the function
        """
        with mock.patch("builtins.input", side_effect=prompt_input):
            return action()

    def generate_metadata(self, user_input: List[str] = None) -> Base:
        """
        Generates a metadata directory and object using mocked user input
        :param user_input: The user input to use
        :return: The generated metadata
        """
        return self.execute_with_mocked_input(
            user_input,
            lambda: self.metadata_cls.generate_from_prompts(self.testdir)
        )

    def verify_metadata(self, json_data: Dict[str, Any], metadata: Base):
        """
        Makes sure that the metadata contents are the same as a json data
        dictionary.
        :param json_data: The JSON data dictionary
        :param metadata: The metadata to check
        :return: None
        """
        metadata_json = metadata.to_json()
        for key in json_data:
            self.assertTrue(key in metadata_json)
            self.assertEqual(metadata_json[key], json_data[key])

    def test_retrieving_verificators(self):
        """
        Tests if the verificator retrieving method is correct
        :return: None
        """
        verificators = self.metadata_cls.get_verifactors()
        for verificator in verificators:
            issubclass(verificator, Verificator)

    def test_generating_using_constructor(self):
        """
        Tests generating a metadata object using the constructor
        :return: None
        """
        metadata = self.metadata_cls(self.json_data_example)
        self.verify_metadata(self.json_data_example, metadata)

    def test_invalid_metadata(self):
        """
        Tests if invalid metadata is correctly identified
        :return: None
        """
        for key in self.json_data_example:
            data = self.json_data_example.copy()
            data.pop(key)

            if "type" not in data:
                continue

            try:
                self.metadata_cls(data)
                print(data)
                self.fail()
            except InvalidMetadataException:
                pass

    def test_metadata_mismatch(self):
        """
        Tests if a metadata mismatch is correctly recognized
        :return: None
        """
        try:
            data = self.json_data_example.copy()
            data["type"] = "other"
            self.metadata_cls(data)
            self.fail()
        except MetadataMismatch:
            pass
