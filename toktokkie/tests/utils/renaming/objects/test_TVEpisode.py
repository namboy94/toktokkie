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
import os
import unittest
from toktokkie.tests.helpers import test_dir, cleanup
from toktokkie.utils.renaming.objects.TVEpisode import TVEpisode
from toktokkie.utils.renaming.schemes.PlexTvdbScheme import PlexTvdbScheme


class TVEpisodeUnitTests(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(test_dir):
            os.makedirs(test_dir)
        with open(os.path.join(test_dir, "episode_file"), 'w'):
            pass

    def tearDown(self):
        cleanup()

    def test_renaming(self):
        episode = TVEpisode(os.path.join(test_dir, "episode_file"), 1, 1, "Game of Thrones", PlexTvdbScheme)
        self.assertTrue(os.path.isfile(os.path.join(test_dir, "episode_file")))
        episode.rename()
        self.assertFalse(os.path.isfile(os.path.join(test_dir, "episode_file")))
        self.assertTrue(os.path.isfile(os.path.join(test_dir, "Game of Thrones - S01E01 - Winter Is Coming")))