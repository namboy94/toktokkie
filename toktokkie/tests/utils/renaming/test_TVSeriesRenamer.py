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

import os
import unittest
from toktokkie.utils.renaming.TVSeriesRenamer import TVSeriesRenamer
from toktokkie.utils.renaming.schemes.PlexTvdbScheme import PlexTvdbScheme
from toktokkie.tests.helpers import create_temp_files_and_folders, cleanup, test_dir


class TVSeriesRenamerUnitTests(unittest.TestCase):

    def setUp(self):
        directories = ["Show 1/.meta", "Show 1/Season 1", "Show 1/Season 2",
                       "Show 2/.meta", "Show 2/Season 1", "Show 2/Season 2", "Show 2/OVA", "Show 2/Specials",
                       "Show 3/.meta", "Show 4"]
        files = ["Show 1/.meta/type", "Show 1/Season 1/aaa.mp4", "Show 1/Season 1/abb.mp4", "Show 1/Season 1/abc.mp4",
                 "Show 1/Season 2/123.mp4", "Show 1/Season 2/456.mp4",
                 "Show 2/.meta/type", "Show 2/Specials/aaa.mp4", "Show 2/Specials/abb.mp4", "Show 2/OVA/abc.mp4",
                 "Show 2/Season 1/123.mp4", "Show 2/Season 2/456.mp4",
                 "Show 3/.meta/type"]
        create_temp_files_and_folders(directories, files)
        with open(os.path.join(test_dir, "Show 1", ".meta", "type"), 'w') as f:
            f.write("tv_series")
        with open(os.path.join(test_dir, "Show 2", ".meta", "type"), 'w') as f:
            f.write("tv_series")
        with open(os.path.join(test_dir, "Show 3", ".meta", "type"), 'w') as f:
            f.write("other")

    def tearDown(self):
        cleanup()
        pass

    def test_constructors(self):
        non_rec_root = TVSeriesRenamer(test_dir, PlexTvdbScheme)
        non_rec_show = TVSeriesRenamer(os.path.join(test_dir, "Show 1"), PlexTvdbScheme)
        rec_root = TVSeriesRenamer(test_dir, PlexTvdbScheme, recursive=True)
        rec_show = TVSeriesRenamer(os.path.join(test_dir, "Show 1"), PlexTvdbScheme, recursive=True)

        self.assertEqual(non_rec_root.episodes, [])
        self.assertEqual(len(non_rec_show.episodes), len(rec_show.episodes))
        self.assertTrue(len(non_rec_show.episodes) < len(rec_root.episodes))

    def test_renaming(self):
        expected_results = ["Show 1/Season 1/Show 1 - S01E01 - Episode 1.mp4",
                            "Show 1/Season 1/Show 1 - S01E02 - Episode 2.mp4",
                            "Show 1/Season 1/Show 1 - S01E03 - Episode 3.mp4",
                            "Show 1/Season 2/Show 1 - S02E01 - Episode 1.mp4",
                            "Show 1/Season 2/Show 1 - S02E02 - Episode 2.mp4"]

        show_one = TVSeriesRenamer(os.path.join(test_dir, "Show 1"), PlexTvdbScheme)

        conf = show_one.request_confirmation()
        for c in conf:
            c.confirm()

        try:
            show_one.start_rename()
            self.assertFalse(True)
        except AssertionError:
            self.assertTrue(True)

        show_one.confirm(conf)
        show_one.start_rename()

        for res in expected_results:
            self.assertTrue(os.path.isfile(os.path.join(test_dir, res)))

    def test_confirmationless_renaming(self):
        expected_results = ["Show 2/Season 1/Show 2 - S01E01 - Episode 1.mp4",
                            "Show 2/Season 2/Show 2 - S02E01 - Episode 1.mp4",
                            "Show 2/Specials/Show 2 - S00E01 - Episode 1.mp4",
                            "Show 2/Specials/Show 2 - S00E02 - Episode 2.mp4",
                            "Show 2/OVA/Show 2 - S00E03 - Episode 3.mp4"]

        show_two = TVSeriesRenamer(os.path.join(test_dir, "Show 2"), PlexTvdbScheme)
        show_two.start_rename(True)

        for res in expected_results:
            self.assertTrue(os.path.isfile(os.path.join(test_dir, res)))

    def test_recursive_renamer_renaming(self):
        expected_results = ["Show 1/Season 1/Show 1 - S01E01 - Episode 1.mp4",
                            "Show 1/Season 1/Show 1 - S01E02 - Episode 2.mp4",
                            "Show 1/Season 1/Show 1 - S01E03 - Episode 3.mp4",
                            "Show 1/Season 2/Show 1 - S02E01 - Episode 1.mp4",
                            "Show 1/Season 2/Show 1 - S02E02 - Episode 2.mp4",
                            "Show 2/Season 1/Show 2 - S01E01 - Episode 1.mp4",
                            "Show 2/Season 2/Show 2 - S02E01 - Episode 1.mp4",
                            "Show 2/Specials/Show 2 - S00E01 - Episode 1.mp4",
                            "Show 2/Specials/Show 2 - S00E02 - Episode 2.mp4",
                            "Show 2/OVA/Show 2 - S00E03 - Episode 3.mp4"]

        recursive_root = TVSeriesRenamer(test_dir, PlexTvdbScheme, recursive=True)
        recursive_root.start_rename(True)

        for res in expected_results:
            self.assertTrue(os.path.isfile(os.path.join(test_dir, res)))
