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
from toktokkie.neometadata.tv.Tv import Tv
from toktokkie.neometadata.tv.components.TvSeason import TvSeason
from toktokkie.test.TestFramework import _TestFramework


class TestTvSeason(_TestFramework):
    """
    Class that tests the TvSeason component
    """

    def test_episode_names(self):
        """
        Tests the episode_names attribute
        :return: None
        """
        otgw = Tv(self.get("Over the Garden Wall"))
        season = otgw.seasons[0]
        episodes = season.episode_names
        self.assertEqual(
            episodes[0],
            "Over the Garden Wall - S01E01 - Chapter 1; The Old Grist Mill"
        )

    def test_missing_attributes(self):
        """
        Tests if missing attributes are handled correctly
        :return: None
        """
        try:
            TvSeason.from_json("1", {}, {})
            self.fail()
        except InvalidMetadata:
            pass
