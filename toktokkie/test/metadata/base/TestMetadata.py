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
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.exceptions import InvalidMetadata, MissingMetadata
from toktokkie.test.TestFramework import _TestFramework


class TestMetadata(_TestFramework):
    """
    Class that tests core functionality of the Metadata class
    """

    def test_missing_metadata_file(self):
        """
        Tests if missing metadata file is detected correctly
        """
        otgw = self.get("Over the Garden Wall")
        meta = Tv(otgw)
        os.remove(meta.metadata_file)

        try:
            Tv(otgw)
            self.fail()
        except MissingMetadata:
            pass

    def test_no_validation(self):
        """
        Tests constructing a metadata object without validation
        :return: None
        """
        otgw = self.get("Over the Garden Wall")
        os.makedirs(os.path.join(otgw, "Season 2"))

        try:
            Tv(otgw)
            self.fail()
        except InvalidMetadata:
            pass

        not_valid = Tv(otgw, no_validation=True)

    def test_repr(self):
        """
        Tests the repr method of the Metadata class
        :return: None
        """
        meta = Tv(self.get("Over the Garden Wall"))
        representation = repr(meta)
        exec(f"self.assertEqual({representation}, meta)")

    def test_trailing_slashes(self):
        """
        Tests if trailing slashes are handled correctly for name parameter
        :return: None
        """
        tv = Tv("test/", {}, no_validation=True)
        self.assertEqual(tv.name, "test")
