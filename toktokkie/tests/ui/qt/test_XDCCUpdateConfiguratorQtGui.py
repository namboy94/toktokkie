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
    from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel
    from PyQt5.QtTest import QTest
    from PyQt5.QtWidgets import QApplication, QFileDialog
    from toktokkie.ui.qt.XDCCUpdateConfiguratorQtGui import XDCCUpdateConfiguratorQtGui
except ImportError:
    Qt = QTest = QFileDialog = QApplication = XDCCUpdateConfiguratorQtGui = None

import os
import sys
import shutil
import unittest
from toktokkie.utils.xdcc.updating.objects.Series import Series


class DummySignal(object):

    def __init__(self, method):
        self.method = method

    def emit(self, *args):
        self.method(*args)


class UnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        if QApplication is None:
            raise unittest.SkipTest("Skipping on import error")

        sys.argv = [sys.argv[0], "-platform", "minimal"]
        cls.app = QApplication(sys.argv)

    def setUp(self):
        sys.argv = [sys.argv[0], "-platform", "minimal"]
        self.form = XDCCUpdateConfiguratorQtGui()
        shutil.copytree(os.path.join("toktokkie", "tests", "resources", "json"), "json_test")

    def tearDown(self):
        self.form.closeEvent(None)
        self.form.destroy()
        shutil.rmtree("json_test")

    def test_loading_json(self):

        old_handler = self.form.json_handler

        # noinspection PyUnusedLocal,PyUnusedLocal,PyShadowingBuiltins
        def browse_file(a, b, filter=""):
            return [os.path.join("json_test", "updater.json")]

        QFileDialog.getOpenFileName = browse_file

        QTest.mouseClick(self.form.load_button, Qt.LeftButton)

        self.assertNotEqual(old_handler, self.form.json_handler)
        self.assertEqual(2, self.form.series_list.count())

    def test_loading_invalid_json_file(self):

        old_handler = self.form.json_handler

        # noinspection PyUnusedLocal,PyUnusedLocal,PyShadowingBuiltins
        def browse_file(a, b, filter=""):
            return [os.path.join("json_test", "invalid.json")]

        QFileDialog.getOpenFileName = browse_file
        QTest.mouseClick(self.form.load_button, Qt.LeftButton)

        self.assertEqual(old_handler, self.form.json_handler)

    def test_adding_new_series(self):
        QTest.mouseClick(self.form.new_button, Qt.LeftButton)
        self.assertEqual(len(self.form.json_handler.get_series()), 1)
        self.assertTrue(self.form.json_handler.get_series()[0].equals(
            Series(os.getcwd(), "New Series", "1080p", "Bot", 1, ["nibl"], "Plex (TVDB)", "horriblesubs")
        ))

    def test_delete_series(self):
        self.test_adding_new_series()
        self.form.series_list.setCurrentRow(0)
        QTest.mouseClick(self.form.delete_button, Qt.LeftButton)

        self.assertEqual(len(self.form.json_handler.get_series()), 0)
