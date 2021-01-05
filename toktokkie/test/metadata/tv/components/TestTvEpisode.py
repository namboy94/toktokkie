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
from toktokkie.metadata.tv.components.TvEpisode import TvEpisode
from toktokkie.test.TestFramework import _TestFramework


class TestTvEpisode(_TestFramework):
    """
    Class that tests the TvEpisode component
    """

    def test_missing_attributes(self):
        """
        Tests if missing attributes are handled correctly
        :return: None
        """
        try:
            TvEpisode.from_json({})
            self.fail()
        except InvalidMetadata:
            pass

    def test_jsonification(self):
        """
        Tests the JSON representation of TvEpisode objects
        :return: None
        """
        episode = TvEpisode(1, 1)
        generated = TvEpisode.from_json(episode.json)
        self.assertEqual(episode.season, generated.season)
        self.assertEqual(episode.episode, generated.episode)
