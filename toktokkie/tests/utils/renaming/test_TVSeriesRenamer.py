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
import shutil
import unittest
from toktokkie.utils.renaming.TVSeriesRenamer import TVSeriesRenamer
from toktokkie.utils.renaming.schemes.PlexTvdbScheme import PlexTvdbScheme


class TVSeriesRenamerUnitTests(unittest.TestCase):

    def setUp(self):
        shutil.copytree("toktokkie/tests/resources/directories", "temp_testing")

    def tearDown(self):
        shutil.rmtree("temp_testing")

    def test_constructors(self):
        non_rec_root = TVSeriesRenamer("temp_testing", PlexTvdbScheme)
        non_rec_show = TVSeriesRenamer(os.path.join("temp_testing", "Game of Thrones"), PlexTvdbScheme)
        rec_root = TVSeriesRenamer("temp_testing", PlexTvdbScheme, recursive=True)
        rec_show = TVSeriesRenamer(os.path.join("temp_testing", "Game of Thrones"), PlexTvdbScheme, recursive=True)

        self.assertEqual(non_rec_root.episodes, [])
        self.assertEqual(len(non_rec_show.episodes), len(rec_show.episodes))
        self.assertTrue(len(non_rec_show.episodes) < len(rec_root.episodes))

    def test_renaming(self):
        expected_results = {"Season 1": ["Game of Thrones - S01E01 - Winter Is Coming",
                                         "Game of Thrones - S01E02 - The Kingsroad",
                                         "Game of Thrones - S01E05 - The Wolf and the Lion",
                                         "Game of Thrones - S01E10 - Fire and Blood",
                                         "Game of Thrones - S01E11 - Episode 11"],
                            "Season 2": ["Game of Thrones - S02E01 - The North Remembers",
                                         "Game of Thrones - S02E10 - Valar Morghulis"],
                            "Specials": ["Game of Thrones - S00E01 - Inside Game of Thrones",
                                         "Game of Thrones - S00E02 - 15-Minute Preview"]}

        game_of_thrones = TVSeriesRenamer(os.path.join("temp_testing", "Game of Thrones"), PlexTvdbScheme)
        confirmation = game_of_thrones.request_confirmation()

        self.assertEqual(len(confirmation), 26)

        try:
            game_of_thrones.start_rename()
            self.assertFalse(True)
        except AssertionError:
            self.assertTrue(True)

        for c in confirmation:
            c.confirm()

        game_of_thrones.confirm(confirmation)
        game_of_thrones.start_rename()

        for result in expected_results:
            for episode in expected_results[result]:
                self.assertTrue(os.path.isfile(os.path.join(
                    "temp_testing", "Game of Thrones", result, episode) + ".mkv"))

    def test_confirmationless_renaming(self):
        expected_results = {"Season 1": ["The Big Bang Theory - S01E01 - Pilot",
                                         "The Big Bang Theory - S01E14 - The Nerdvana Annihilation"],
                            "Season 2": ["The Big Bang Theory - S02E05 - The Euclid Alternative",
                                         "The Big Bang Theory - S02E13 - The Friendship Algorithm"],
                            "Season 3": ["The Big Bang Theory - S03E07 - The Guitarist Amplification",
                                         "The Big Bang Theory - S03E10 - The Gorilla Experiment"],
                            "Season 4": ["The Big Bang Theory - S04E01 - The Robotic Manipulation",
                                         "The Big Bang Theory - S04E06 - The Irish Pub Formulation"],
                            "Season 5": ["The Big Bang Theory - S05E08 - The Isolation Permutation",
                                         "The Big Bang Theory - S05E13 - The Recombination Hypothesis"]}

        big_bang = TVSeriesRenamer(os.path.join("temp_testing", "The Big Bang Theory"), PlexTvdbScheme)
        confirmation = big_bang.request_confirmation()
        self.assertEqual(len(confirmation), 120)
        big_bang.start_rename(True)

        for result in expected_results:
            for episode in expected_results[result]:
                self.assertTrue(os.path.isfile(os.path.join(
                    "temp_testing", "The Big Bang Theory", result, episode) + ".mkv"))

    def test_recursive_renamer_renaming(self):
        expected_game_of_thrones_results = {"Season 1": ["Game of Thrones - S01E01 - Winter Is Coming",
                                                         "Game of Thrones - S01E02 - The Kingsroad",
                                                         "Game of Thrones - S01E05 - The Wolf and the Lion",
                                                         "Game of Thrones - S01E10 - Fire and Blood",
                                                         "Game of Thrones - S01E11 - Episode 11"],
                                            "Season 2": ["Game of Thrones - S02E01 - The North Remembers",
                                                         "Game of Thrones - S02E10 - Valar Morghulis"],
                                            "Specials": ["Game of Thrones - S00E01 - Inside Game of Thrones",
                                                         "Game of Thrones - S00E02 - 15-Minute Preview"]}
        expected_big_bang_theory_results = {"Season 1": ["The Big Bang Theory - S01E01 - Pilot",
                                                         "The Big Bang Theory - S01E14 - The Nerdvana Annihilation"],
                                            "Season 2": ["The Big Bang Theory - S02E05 - The Euclid Alternative",
                                                         "The Big Bang Theory - S02E13 - The Friendship Algorithm"],
                                            "Season 3": ["The Big Bang Theory - S03E07 - The Guitarist Amplification",
                                                         "The Big Bang Theory - S03E10 - The Gorilla Experiment"],
                                            "Season 4": ["The Big Bang Theory - S04E01 - The Robotic Manipulation",
                                                         "The Big Bang Theory - S04E06 - The Irish Pub Formulation"],
                                            "Season 5": ["The Big Bang Theory - S05E08 - The Isolation Permutation",
                                                         "The Big Bang Theory - S05E13 - The Recombination Hypothesis"]}

        recursive_root = TVSeriesRenamer("temp_testing", PlexTvdbScheme, recursive=True)
        recursive_root.start_rename(True)

        for result in expected_game_of_thrones_results:
            for episode in expected_game_of_thrones_results[result]:
                self.assertTrue(os.path.isfile(os.path.join(
                    "temp_testing", "Game of Thrones", result, episode) + ".mkv"))
        for result in expected_big_bang_theory_results:
            for episode in expected_big_bang_theory_results[result]:
                self.assertTrue(os.path.isfile(os.path.join(
                    "temp_testing", "The Big Bang Theory", result, episode) + ".mkv"))

    def test_unconfirmed_renaming(self):
        renamer = TVSeriesRenamer(os.path.join("temp_testing", "Game of Thrones"), PlexTvdbScheme)
        confirmation = renamer.request_confirmation()
        renamer.confirm(confirmation)
        renamer.start_rename()

        self.assertTrue(os.path.isfile(os.path.join("temp_testing", "Game of Thrones", "Season 1", "Episode 01.mkv")))
        self.assertFalse(os.path.isfile(os.path.join("temp_testing", "Game of Thrones", "Season 1",
                                                     "Game of Thrones - S01E01 - Winter Is Coming")))

