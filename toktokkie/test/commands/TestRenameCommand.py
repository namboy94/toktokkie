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
from toktokkie.test.TestFramework import _TestFramework


class TestRenameCommand(_TestFramework):
    """
    Class that tests the rename command
    """

    def test_renaming(self):
        """
        Tests simply renaming using the rename command
        :return: None
        """
        path = self.get("Over the Garden Wall")

        old, new = self.scramble_episode_names(path)
        for entry in old:
            self.assertFalse(os.path.isfile(entry))
        for entry in new:
            self.assertTrue(os.path.isfile(entry))

        self.execute_command(["rename", path], ["y"])

        for entry in old:
            self.assertTrue(os.path.isfile(entry))
        for entry in new:
            self.assertFalse(os.path.isfile(entry))

    def test_renaming_title(self):
        """
        Tests renaming the title of the directory
        :return:  None
        """
        path = self.get("Over the Garden Wall")
        renamed = self.get("Renamed")
        os.rename(path, renamed)

        self.assertFalse(os.path.isdir(path))
        self.assertTrue(os.path.isdir(renamed))

        self.execute_command(
            ["rename", renamed, "--include-title"],
            ["y", "y"]
        )
        self.assertTrue(os.path.isdir(path))
        self.assertFalse(os.path.isdir(renamed))

    def test_renaming_with_noconfirm(self):
        """
        Tests renaming without confirmation
        :return: None
        """
        path = self.get("Over the Garden Wall")
        renamed = self.get("Over the Garden Fence")

        target, _ = self.scramble_episode_names(path)
        os.rename(path, renamed)

        self.execute_command(
            ["rename", renamed, "--include-title", "--noconfirm"],
            []
        )

        for entry in target:
            self.assertTrue(os.path.isfile(entry))
