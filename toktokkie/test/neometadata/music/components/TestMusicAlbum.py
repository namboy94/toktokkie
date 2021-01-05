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

from toktokkie.exceptions import InvalidMetadata
from toktokkie.neometadata.music.components.MusicAlbum import MusicAlbum
from toktokkie.test.TestFramework import _TestFramework


class TestMusicAlbum(_TestFramework):
    """
    Class that tests the MusicAlbum class
    """

    def test_missing_json_attributes(self):
        """
        Tests if missing JSON attributes are detected correctly
        :return: None
        """
        try:
            MusicAlbum.from_json("", {}, {})
            self.fail()
        except InvalidMetadata:
            pass
