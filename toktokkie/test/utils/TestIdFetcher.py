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

from unittest.mock import patch
from toktokkie.enums import MediaType, IdType
from toktokkie.utils.IdFetcher import IdFetcher
from toktokkie.test.TestFramework import _TestFramework


class TestIdFetcher(_TestFramework):
    """
    Tests the IdFetcher class
    """

    def test_tvdb_name_fetching(self):
        """
        Tests fetching tvdb IDs based on name
        :return: None
        """
        fetcher = IdFetcher("Fullmetal Alchemist (2003)", MediaType.TV_SERIES)
        self.assertEqual(
            fetcher.fetch_ids(IdType.TVDB, {}),
            ["75579"]
        )

    def test_imdb_name_fetching(self):
        """
        Tests fetching IMDB IDs based on name
        :return: None
        """
        fetcher = IdFetcher("Fullmetal Alchemist (2003)", MediaType.TV_SERIES)
        self.assertEqual(
            fetcher.fetch_ids(IdType.IMDB, {}),
            ["tt0421357"]
        )
        fetcher = IdFetcher("Hataraku Saibou: Code Black", MediaType.TV_SERIES)
        self.assertIsNone(fetcher.fetch_ids(IdType.IMDB, {}))

    def test_imdb_fetching_with_tvdb(self):
        """
        Tests fetching IMDB IDs using TVDB IDs
        :return: None
        """
        fetcher = IdFetcher("", MediaType.TV_SERIES)
        self.assertEqual(
            fetcher.fetch_ids(IdType.IMDB, {IdType.TVDB: ["75579"]}),
            ["tt0421357"]
        )

    def test_anilist_fetching_with_myanimelist(self):
        """
        Tests fetching anilist IDs using Myanimelist IDs
        :return: None
        """
        fetcher = IdFetcher("", MediaType.TV_SERIES)
        self.assertEqual(
            fetcher.fetch_ids(IdType.ANILIST, {IdType.MYANIMELIST: ["39586"]}),
            ["108631"]
        )
        fetcher.media_type = MediaType.COMIC
        self.assertEqual(
            fetcher.fetch_ids(
                IdType.ANILIST, {IdType.MYANIMELIST: ["112589"]}
            ),
            ["101177"]
        )

    def test_myanimelist_fetching_with_anilist(self):
        """
        Tests fetching myanimelist IDs using anilist IDs
        :return: None
        """
        fetcher = IdFetcher("", MediaType.TV_SERIES)
        self.assertEqual(
            fetcher.fetch_ids(
                IdType.MYANIMELIST, {IdType.ANILIST: ["108631"]}
            ),
            ["39586"]
        )
        fetcher.media_type = MediaType.COMIC
        self.assertEqual(
            fetcher.fetch_ids(
                IdType.MYANIMELIST, {IdType.ANILIST: ["101177"]}
            ),
            ["112589"]
        )
        self.assertIsNone(fetcher.fetch_ids(
            IdType.MYANIMELIST, {IdType.ANILIST: ["128328"]}
        ))

    def test_anilist_fetching_with_mangadex(self):
        """
        Tests fetching anilist IDs using mangadex IDs
        :return: None
        """
        fetcher = IdFetcher("", MediaType.TV_SERIES)
        self.assertEqual(
            fetcher.fetch_ids(IdType.ANILIST, {IdType.MANGADEX: ["23439"]}),
            ["101177"]
        )

    def test_myanimelist_fetching_with_mangadex(self):
        """
        Tests fetching myanimelist IDs using mangadex IDs
        :return: None
        """
        fetcher = IdFetcher("", MediaType.COMIC)
        self.assertEqual(
            fetcher.fetch_ids(
                IdType.MYANIMELIST, {IdType.MANGADEX: ["23439"]}
            ),
            ["112589"]
        )

    def test_musicbrainz_artist_by_name(self):
        """
        Tests fetching musicbrainz ID using the artist name
        :return: None
        """
        fetcher = IdFetcher("Aimer", MediaType.MUSIC_ARTIST)
        self.assertEqual(
            fetcher.fetch_ids(IdType.MUSICBRAINZ_ARTIST, {}),
            ["9388cee2-7d57-4598-905f-106019b267d3"]
        )
        fetcher = IdFetcher("Aimér", MediaType.MUSIC_ARTIST)
        self.assertEqual(
            fetcher.fetch_ids(IdType.MUSICBRAINZ_ARTIST, {}),
            ["0"]
        )
        fetcher = IdFetcher("Hasshsjahhjajujjaja", MediaType.MUSIC_ARTIST)
        self.assertEqual(
            fetcher.fetch_ids(IdType.MUSICBRAINZ_ARTIST, {}),
            ["0"]
        )

    def test_unsupported_fetching(self):
        """
        Tests fetching unsupported IDs + ID combinations
        :return: None
        """
        fetcher = IdFetcher("", MediaType.TV_SERIES)
        self.assertIsNone(fetcher.fetch_ids(IdType.KITSU, {}))
        self.assertIsNone(fetcher.fetch_ids(IdType.ANILIST, {}))
        self.assertIsNone(fetcher.fetch_ids(IdType.MYANIMELIST, {}))

    def test_error_handling(self):
        """
        Tests if any errors are caught
        :return: None
        """
        fetcher = IdFetcher("", MediaType.TV_SERIES)
        with patch("toktokkie.utils.IdFetcher.tvdb_api", lambda x: 1/0):
            self.assertIsNone(fetcher.fetch_ids(IdType.TVDB, {}))

    def test_tvdb_error_handling(self):
        """
        Tests tvdb error handling
        :return: None
        """
        class DummyTvdb:
            tvdb_shownotfound = ZeroDivisionError
            to_raise = ValueError()

            # noinspection PyPep8Naming
            def Tvdb(self):
                raise self.to_raise

        dummy = DummyTvdb()
        fetcher = IdFetcher("", MediaType.TV_SERIES)
        with patch("toktokkie.utils.IdFetcher.tvdb_api", dummy):
            self.assertIsNone(fetcher.fetch_ids(IdType.TVDB, {}))
            self.assertIsNone(fetcher.fetch_ids(
                IdType.IMDB, {IdType.TVDB: ["1"]}
            ))
        dummy.to_raise = TypeError()
        with patch("toktokkie.utils.IdFetcher.tvdb_api", dummy):
            self.assertIsNone(fetcher.fetch_ids(IdType.TVDB, {}))
            self.assertIsNone(fetcher.fetch_ids(
                IdType.IMDB, {IdType.TVDB: ["1"]}
            ))

    def test_empty_other_ids(self):
        """
        Tests if empty ID list are ignored successfully
        :return: None
        """
        fetcher = IdFetcher("", MediaType.COMIC)
        self.assertEqual(
            fetcher.fetch_ids(IdType.ANILIST, {
                IdType.MANGADEX: ["23439"],
                IdType.MYANIMELIST: []
            }),
            ["101177"]
        )
