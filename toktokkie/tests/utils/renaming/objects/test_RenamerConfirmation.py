"""
Copyright 2015-2017 Hermann Krumrey

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
"""

# imports
import os
import shutil
import unittest
from toktokkie.utils.renaming.objects.TVEpisode import TVEpisode
from toktokkie.utils.renaming.schemes.PlexTvdbScheme import PlexTvdbScheme
from toktokkie.utils.renaming.objects.RenamerConfirmation import \
    RenamerConfirmation


class RenamerConfirmationUnitTests(unittest.TestCase):

    def setUp(self):
        os.makedirs("temp_testing")
        with open(os.path.join("temp_testing", "episode_file"), 'w'):
            pass
        self.episode = TVEpisode(
            os.path.join("temp_testing", "episode_file"), 1, 1,
            "Game of Thrones", PlexTvdbScheme
        )

    def tearDown(self):
        shutil.rmtree("temp_testing")

    def test_wrapper(self):
        confirmer = RenamerConfirmation(self.episode)
        self.assertEqual(confirmer.get_episode(), self.episode)
        self.assertEqual(confirmer.get_names()[0], self.episode.get_old_name())
        self.assertEqual(confirmer.get_names()[1], self.episode.get_new_name())
        self.assertEqual(
            confirmer.get_names(),
            ("episode_file", "Game of Thrones - S01E01 - Winter Is Coming")
        )

    def test_confirming(self):
        confirmer = RenamerConfirmation(self.episode)
        self.assertFalse(confirmer.get_confirmed_status())
        confirmer.confirm()
        self.assertTrue(confirmer.get_confirmed_status())
