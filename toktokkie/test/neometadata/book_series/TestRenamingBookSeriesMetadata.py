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
from unittest.mock import patch
from puffotter.os import listdir
from toktokkie.Directory import Directory
from toktokkie.neometadata.book_series.BookSeries import BookSeries
from toktokkie.test.TestFramework import _TestFramework


class TestRenamingBookSeriesMetadata(_TestFramework):
    """
    Class that tests the BookSeriesRenamer class
    """

    def test_renaming_book_series(self):
        """
        Tests renaming a book series
        :return: None
        """
        bluesteel = self.get("Bluesteel Blasphemer")
        meta = BookSeries(bluesteel)

        original = []
        new = []

        for name, path in listdir(bluesteel, no_dirs=True):
            original.append(path)
            new.append(os.path.join(bluesteel, "A" + name))
            os.rename(path, new[-1])

        for entry in original:
            self.assertFalse(os.path.isfile(entry))
        for entry in new:
            self.assertTrue(os.path.isfile(entry))

        meta.rename(noconfirm=True, skip_title=True)

        for entry in original:
            self.assertTrue(os.path.isfile(entry))
        for entry in new:
            self.assertFalse(os.path.isfile(entry))

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
        with patch("builtins.input", side_effect=[
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
