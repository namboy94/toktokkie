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

from toktokkie.metadata.tv.Tv import Tv
from toktokkie.enums import IdType
from toktokkie.metadata.tv.components.TvSeason import TvSeason
from toktokkie.test.TestFramework import _TestFramework


class TestTvExtras(_TestFramework):
    """
    Class that tests the extra features of tv series metadata objects
    """

    def test_seasons(self):
        """
        Tests retrieving season information
        :return: None
        """
        meta = Tv(self.get("Fullmetal Alchemist"))

        seasons = meta.seasons
        self.assertEqual(len(seasons), 3)

        season_1 = seasons[0]
        self.assertEqual(season_1.name, "Season 1")
        self.assertEqual(season_1.ids[IdType.IMDB], ["tt0421357"])
        self.assertEqual(season_1.ids[IdType.MYANIMELIST], ["121"])

        new_season = TvSeason(
            meta.directory_path, meta.ids, {IdType.KITSU: ["100"]}, "Test"
        )
        seasons.append(new_season)

        meta.seasons = seasons

        fetched_new_season = meta.get_season("Test")
        self.assertEqual(fetched_new_season.name, "Test")
        self.assertEqual(fetched_new_season.ids[IdType.IMDB], ["tt0421357"])
        self.assertEqual(fetched_new_season.ids[IdType.KITSU], ["100"])

        relections = meta.get_season("Fullmetal Alchemist - Reflections")
        self.assertEqual(relections.ids[IdType.MYANIMELIST], ["664"])

        try:
            meta.get_season("Doesn't exist")
            self.fail()
        except KeyError:
            pass

    def test_excluding(self):
        """
        Tests excluding episodes
        :return: None
        """
        meta = Tv(self.get("Over the Garden Wall"))

        excluded = meta.excludes
        self.assertEqual(len(excluded), 0)

        meta.add_exclude(IdType.IMDB, 1, 1)
        excluded = meta.excludes
        self.assertEqual(excluded[IdType.IMDB][1], [1])

        meta.add_exclude(IdType.IMDB, 1, 2)
        excluded = meta.excludes
        self.assertEqual(excluded[IdType.IMDB][1], [1, 2])

        meta.add_exclude(IdType.IMDB, 1, 5, 8)
        excluded = meta.excludes
        self.assertEqual(excluded[IdType.IMDB][1], [1, 2, 5, 6, 7, 8])

    def test_season_start_overrides(self):
        """
        Tests season start overrides
        :return: None
        """
        meta = Tv(self.get("Over the Garden Wall"))

        overrides = meta.season_start_overrides
        self.assertEqual(len(overrides), 0)

        meta.add_season_start_override(IdType.IMDB, 1, 5)

        overrides = meta.season_start_overrides
        self.assertEqual(len(overrides), 1)
        self.assertEqual(len(overrides[IdType.IMDB]), 1)
        self.assertEqual(overrides[IdType.IMDB][1], 5)

        meta.add_season_start_override(IdType.IMDB, 1, 8)
        overrides = meta.season_start_overrides
        self.assertEqual(len(overrides), 1)
        self.assertEqual(len(overrides[IdType.IMDB]), 1)
        self.assertEqual(overrides[IdType.IMDB][1], 8)

    def test_multi_episodes(self):
        """
        Tests multi-episodes
        :return: None
        """
        meta = Tv(self.get("Over the Garden Wall"))
        self.assertEqual(len(meta.multi_episodes), 0)

        meta.add_multi_episode(IdType.IMDB, 1, 1, 2)
        multis = meta.multi_episodes
        self.assertEqual(len(multis), 1)
        self.assertEqual(len(multis[IdType.IMDB]), 1)
        self.assertEqual(len(multis[IdType.IMDB][1]), 1)
        self.assertEqual(meta.multi_episodes[IdType.IMDB][1][1], 2)

        meta.add_multi_episode(IdType.IMDB, 1, 3, 4)
        multis = meta.multi_episodes
        self.assertEqual(len(multis), 1)
        self.assertEqual(len(multis[IdType.IMDB]), 1)
        self.assertEqual(len(multis[IdType.IMDB][1]), 2)
        self.assertEqual(meta.multi_episodes[IdType.IMDB][1][1], 2)
        self.assertEqual(meta.multi_episodes[IdType.IMDB][1][3], 4)

    def test_urls(self):
        """
        Tests the Urls parameter
        :return: None
        """
        meta = Tv(self.get("Fullmetal Alchemist"))
        urls = meta.urls
        self.assertEqual(
            urls[IdType.TVDB],
            ["https://www.thetvdb.com/?id=75579&tab=series"]
        )
        self.assertEqual(
            urls[IdType.IMDB],
            ["https://www.imdb.com/title/tt0421357"]
        )
        self.assertEqual(
            urls[IdType.MYANIMELIST],
            ["https://myanimelist.net/anime/121",
             "https://myanimelist.net/anime/664",
             "https://myanimelist.net/anime/430"]
        )
        self.assertEqual(
            urls[IdType.ANILIST],
            ["https://anilist.co/anime/121",
             "https://anilist.co/anime/664",
             "https://anilist.co/anime/430"]
        )
