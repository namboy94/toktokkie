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
from toktokkie.metadata.music.components.MusicAlbum import MusicAlbum
from toktokkie.metadata.music.components.MusicThemeSong import \
    MusicThemeSong
from toktokkie.test.TestFramework import _TestFramework


class TestMusicThemeSong(_TestFramework):
    """
    Class that tests the MusicThemeSong class
    """

    def test_missing_json_attributes(self):
        """
        Tests if missing JSON attributes are detected correctly
        :return: None
        """
        try:
            # noinspection PyTypeChecker
            MusicThemeSong.from_json(None, {})
            self.fail()
        except InvalidMetadata:
            pass

    def test_unmatched_album(self):
        """
        Tests if unmatched album names cause warnings
        :return: None
        """
        album = MusicAlbum("", {}, {}, "A", "", 2020)

        class DummyLogger:
            # noinspection PyMethodMayBeStatic
            def warning(self, _):
                print(1 / 0)

        class DummyThemeSong(MusicThemeSong):
            logger = DummyLogger()

        try:
            DummyThemeSong(album, "B", "", {})
            self.fail()
        except ZeroDivisionError:
            pass
