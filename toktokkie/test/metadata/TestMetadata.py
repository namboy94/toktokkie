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

from toktokkie.test.TestFramework import _TestFramework


class _TestMetadata(_TestFramework):
    """
    Class that defines what a metadata test has to test
    """

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        raise NotImplementedError()

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        raise NotImplementedError()

    def test_invalid_metadata(self):
        """
        Tests if invalid metadata is identified correctly
        :return: None
        """
        raise NotImplementedError()

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        raise NotImplementedError()

    def test_checking(self):
        """
        Tests if the checking mechanisms work correctly
        :return: None
        """
        raise NotImplementedError()
