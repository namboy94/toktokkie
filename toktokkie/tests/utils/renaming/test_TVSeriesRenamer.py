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

import shutil
import unittest
from toktokkie.utils.renaming.TVSeriesRenamer import TVSeriesRenamer
from toktokkie.tests.helpers import create_temporary_tv_series_directories
from toktokkie.utils.renaming.schemes.PlexTvdbScheme import PlexTvdbScheme


class TVSeriesRenamerUnitTests(unittest.TestCase):

    def setUp(self):
        self.temporary_directory = create_temporary_tv_series_directories()

    def tearDown(self):
        shutil.rmtree(self.temporary_directory)

    def test_constructors(self):
        TVSeriesRenamer(self.temporary_directory, PlexTvdbScheme)
        TVSeriesRenamer(self.temporary_directory, PlexTvdbScheme, recursive=True)

    def test_stuff(self):
        pass
