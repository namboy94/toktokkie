"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

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
LICENSE
"""

# imports
try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtTest import QTest
    from PyQt5.QtWidgets import QApplication
    from toktokkie.ui.qt.TVSeriesRenamerQtGui import TVSeriesRenamerQtGui
except ImportError:
    Qt = QTest = TVSeriesRenamerQtGui = QApplication = None

import os
import sys
import shutil
import unittest


class UnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        if QApplication is None:
            raise unittest.SkipTest("Skipping on python 2 or import error")

        sys.argv = [sys.argv[0], "-platform", "minimal"]
        cls.app = QApplication(sys.argv)

    def setUp(self):
        sys.argv = [sys.argv[0], "-platform", "minimal"]
        self.form = TVSeriesRenamerQtGui()
        shutil.copytree(os.path.join("toktokkie", "tests", "resources", "directories"), "temp_testing")

    def tearDown(self):
        self.form.destroy()
        shutil.rmtree("temp_testing")

    def test_directory_parsing_non_recursive(self):

        self.assertTrue(self.form.meta_warning_label.isVisibleTo(self.form))

        if self.form.recursive_check.checkState():
            self.form.recursive_check.nextCheckState()

        self.form.directory_entry.setText("temp_testing")
        self.assertEqual(self.form.rename_list.topLevelItemCount(), 0)
        self.assertTrue(self.form.meta_warning_label.isVisibleTo(self.form))

        self.form.directory_entry.setText(os.path.join("temp_testing", "Game of Thrones"))
        self.assertEqual(self.form.rename_list.topLevelItemCount(), 26)
        self.assertFalse(self.form.meta_warning_label.isVisibleTo(self.form))

    def test_diectory_parsing_recursive(self):

        self.form.directory_entry.setText("temp_testing")

        if not self.form.recursive_check.checkState():
            self.form.recursive_check.nextCheckState()

        self.assertLess(26, self.form.rename_list.topLevelItemCount())
        self.assertFalse(self.form.meta_warning_label.isVisibleTo(self.form))

    def test_remove_selection(self):
        self.test_directory_parsing_non_recursive()
        self.form.rename_list.selectAll()
        QTest.mouseClick(self.form.selection_remover_button, Qt.LeftButton)

        self.assertEqual(0, self.form.rename_list.topLevelItemCount())

    def test_renaming(self):
        self.test_directory_parsing_non_recursive()
        previous_item_amount = self.form.rename_list.topLevelItemCount()

        QTest.mouseClick(self.form.confirm_button, Qt.LeftButton)

        self.assertTrue(os.path.isfile(os.path.join("temp_testing", "Game of Thrones", "Season 1",
                                                    "Game of Thrones - S01E01 - Winter Is Coming.mkv")))
        self.assertEqual(previous_item_amount, self.form.rename_list.topLevelItemCount())
