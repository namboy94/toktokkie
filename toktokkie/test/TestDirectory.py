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
import json
import shutil
from puffotter.os import makedirs
from unittest.mock import patch
from toktokkie.enums import MediaType
from toktokkie.Directory import Directory
from toktokkie.exceptions import InvalidMetadata
from toktokkie.test.TestFramework import _TestFramework


class TestDirectory(_TestFramework):
    """
    Class that tests the directory class
    """

    def test_loading_reloading_saving(self):
        """
        Tests loading, reloading and saving directory metadata
        :return: None
        """
        directory = Directory(self.get("AmaLee"))
        self.assertEqual(directory.metadata.tags, [])

        directory.metadata.tags = ["one"]
        directory.save()
        directory.metadata.tags = []
        directory.reload()
        self.assertEqual(directory.metadata.tags, ["one"])

    def test_prompting(self):
        """
        Tests prompting for new metadata using the Directory class
        :return: None
        """
        path = self.get("Princess Evangile")
        makedirs(path)
        with patch("builtins.input", side_effect=[
            "one, two",
            "100"
        ]):
            directory = Directory.prompt(path, "game")

        self.assertEqual(directory.metadata.tags, ["one", "two"])
        self.assertTrue(os.path.isdir(directory.metadata.directory_path))
        self.assertEqual(directory.path, path)

    def test_overwriting_exisiting_metadata(self):
        """
        Tests overwriting existing metadata
        :return: None
        """
        path = self.get("Fureraba")
        existing = Directory(path)

        with patch("builtins.input", side_effect=[
            "n"
        ]):
            directory = Directory.prompt(path, MediaType.GAME)
            self.assertIsNone(directory)

        with patch("builtins.input", side_effect=[
            "y",
            "one, two",
            "100"
        ]):
            directory = Directory.prompt(path, MediaType.GAME)
            self.assertIsNotNone(directory)

        self.assertEqual(directory.metadata.tags, ["one", "two"])
        self.assertNotEqual(directory.metadata.tags, existing.metadata.tags)

    def test_getting_metadata_without_media_type_in_json(self):
        """
        Tests if a missing media type is caught correctly
        :return: None
        """
        directory = Directory(self.get("Faust"))
        json_data = directory.metadata.json
        json_data.pop("type")

        with open(directory.metadata.metadata_file, "w") as f:
            json.dump(json_data, f)

        try:
            Directory(self.get("Faust"))
            self.fail()
        except InvalidMetadata:
            pass

    def test_loading_directories(self):
        """
        Tests loading directories
        :return: None
        """
        base_path = os.path.dirname(self.get("test"))
        all_dirs = Directory.load_child_directories(base_path)
        self.assertEqual(len(all_dirs), len(os.listdir(base_path)))

        music_dirs = Directory.load_child_directories(
            base_path, [MediaType.MUSIC_ARTIST]
        )
        self.assertEqual(len(music_dirs), 2)

        faust = Directory(self.get("Faust"))
        json_data = faust.metadata.json
        json_data.pop("type")

        with open(faust.metadata.metadata_file, "w") as f:
            json.dump(json_data, f)

        shutil.rmtree(self.get("AmaLee"))
        makedirs(self.get("AmaLee"))

        less_dirs = Directory.load_child_directories(base_path)
        self.assertEqual(len(less_dirs), len(os.listdir(base_path)) - 2)
