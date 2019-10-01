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
import tvdb_api
from toktokkie.Directory import Directory
from toktokkie.exceptions import InvalidMetadata
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.test.metadata.TestMetadata import _TestMetadata


class TestTvSeries(_TestMetadata):
    """
    Test class for TV metadata
    """

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        pass

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        pass

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        pass

    def test_checking(self):
        """
        Tests if the checking mechanisms work correctly
        :return: None
        """
        pass
