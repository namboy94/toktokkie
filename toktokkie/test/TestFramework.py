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
import unittest
from jsonschema import validate, ValidationError
from typing import Tuple, List, Any, Dict, Type
from puffotter.os import listdir
from toktokkie.neometadata.base.Validator import Validator


class _TestFramework(unittest.TestCase):
    """
    A class that implements standard setUp and tearDown methods for unit tests
    """

    resources = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "res"
    )
    """
    The directory containing the original test resources.
    The contents of this directory should not be modified during tests.
    """

    res_dir = "/tmp/toktokkie-test-res"
    """
    The directory containing a fresh copy of the test resources.
    May be modified during tests. Regenerated in setUp method.
    """

    def cleanup(self):
        """
        Deletes any generated resources
        :return:
        """
        if os.path.exists(self.res_dir):
            shutil.rmtree(self.res_dir)

    def setUp(self):
        """
        Sets up the test resources
        :return: None
        """
        self.cleanup()
        try:
            shutil.copytree(self.resources, self.res_dir)
        except FileNotFoundError:
            shutil.copytree(os.path.basename(self.resources), self.res_dir)

    def tearDown(self):
        """
        Deletes the test resources
        :return: None
        """
        self.cleanup()

    def get(self, directory: str) -> str:
        """
        Retrieves the path to a test resource
        :param directory: The directory to get
        :return: The path to the directory
        """
        return os.path.join(self.res_dir, directory)

    def assert_directories_same(self, should_dir: str, is_dir: str):
        """
        Makes sure that two directories share the same content.
        :param should_dir: The first directory
        :param is_dir: The second directory
        :return: None
        """
        self.assertTrue(os.path.isdir(should_dir))
        self.assertTrue(os.path.isdir(is_dir))
        should_children = os.listdir(should_dir)
        is_children = os.listdir(is_dir)

        self.assertEqual(len(should_children), len(is_children))

        for child in should_children:
            self.assertTrue(child in is_children)
            child_path = os.path.join(should_dir, child)

            if os.path.isdir(child_path):
                self.assert_directories_same(
                    child_path, os.path.join(is_dir, child)
                )

    def scramble_episode_names(self, directory: str) \
            -> Tuple[List[str], List[str]]:
        """
        Scrambles the existing episode names to ease checking of correct
        renaming
        :param directory: The directory whose contents to scramble
        :return: A list containing paths to the correct and scrambled files
        """
        correct = []
        wrong = []
        for _, season_dir in listdir(directory, no_files=True):
            for episode, episode_file in listdir(season_dir, no_dirs=True):
                new_file = os.path.join(season_dir, "A" + episode)
                os.rename(episode_file, new_file)
                correct.append(episode_file)
                wrong.append(new_file)

        for _file in correct:
            self.assertFalse(os.path.isfile(_file))
        for _file in wrong:
            self.assertTrue(os.path.isfile(_file))

        return correct, wrong

    def perform_json_validation(
            self,
            metadata_cls: Type[Validator],
            valid_json: List[Dict[str, Any]],
            invalid_json: List[Dict[str, Any]]
    ):
        """
        Performs validation checks for json schemas
        :param metadata_cls: The metadata validator class
        :param valid_json: Valid json dictionaries
        :param invalid_json: Invalid JSON dictionaries
        :return: None
        """
        schema = metadata_cls.build_schema()
        print("Valid")
        for entry in valid_json:
            print(entry)
            validate(entry, schema)
        print("Invalid")
        for entry in invalid_json:
            print(entry)
            try:
                validate(entry, schema)
                self.fail()
            except ValidationError:
                pass
