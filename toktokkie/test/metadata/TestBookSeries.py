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
from unittest import mock
from toktokkie.Directory import Directory
from toktokkie.metadata.BookSeries import BookSeries
from toktokkie.test.metadata.TestMetadata import _TestMetadata
from puffotter.os import listdir


class TestBookSeries(_TestMetadata):
    """
    Class that tests the BookSeries metadata class
    """

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        bsb = self.get("Bluesteel Blasphemer")
        bsb_dir = Directory(bsb)

        correct_files = []
        incorrect_files = []
        for volume, path in listdir(bsb):

            new_file = os.path.join(bsb, "AAA" + volume)
            os.rename(path, new_file)

            correct_files.append(path)
            incorrect_files.append(new_file)
            self.assertFalse(os.path.isfile(path))
            self.assertTrue(os.path.isfile(new_file))

        bsb_dir.rename(noconfirm=True)

        for correct_file in correct_files:
            self.assertTrue(os.path.isfile(correct_file))
        for incorrect_file in incorrect_files:
            self.assertFalse(os.path.isfile(incorrect_file))

        bsb_dir.metadata.name = "Not Bluesteel Blasphemer"
        with mock.patch("builtins.input", side_effect=[
            "n", "y"
        ]):
            bsb_dir.rename()

        self.assertTrue(os.path.isdir(self.get("Not Bluesteel Blasphemer")))
        self.assertFalse(os.path.isdir(bsb))

        for correct_file in correct_files:
            self.assertFalse(os.path.isfile(correct_file))
            self.assertTrue(os.path.isfile(correct_file.replace(
                "Bluesteel Blasphemer", "Not Bluesteel Blasphemer"
            )))

        bsb_dir.rename(noconfirm=True)

        for correct_file in correct_files:
            self.assertTrue(os.path.isfile(correct_file))
            self.assertFalse(os.path.isfile(correct_file.replace(
                "Bluesteel Blasphemer", "Not Bluesteel Blasphemer"
            )))

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        raise NotImplementedError()

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        raise NotImplementedError()

    def test_checking(self):
        """
        Tests if the checking mechanisms work correctly
        :return: None
        """
        raise NotImplementedError()
