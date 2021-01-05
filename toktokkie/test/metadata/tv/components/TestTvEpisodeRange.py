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
from toktokkie.metadata.tv.components.TvEpisodeRange import TvEpisodeRange
from toktokkie.test.TestFramework import _TestFramework


class TestTvEpisodeRange(_TestFramework):
    """
    Class that tests the TvEpisodeRange component
    """

    def test_missing_attributes(self):
        """
        Tests if missing attributes are handled correctly
        :return: None
        """
        try:
            TvEpisodeRange.from_json({})
            self.fail()
        except InvalidMetadata:
            pass

    def test_jsonification(self):
        """
        Tests the JSON representation of TvEpisodeRange objects
        :return: None
        """
        episode_range = TvEpisodeRange(1, 1, 10)
        generated = TvEpisodeRange.from_json(episode_range.json)
        self.assertEqual(episode_range.season, generated.season)
        self.assertEqual(episode_range.start_episode, generated.start_episode)
        self.assertEqual(episode_range.end_episode, generated.end_episode)