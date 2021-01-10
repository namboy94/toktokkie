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

from typing import Optional, List
from toktokkie.enums import IdType
from toktokkie.Directory import Directory
from toktokkie.test.TestFramework import _TestFramework
from toktokkie.metadata.tv.Tv import Tv


class TestIdFetchCommand(_TestFramework):
    """
    Class that tests the id-fetch command
    """

    def execute_id_fetch_check(
            self,
            name: str,
            id_type: IdType,
            expected_id: str,
            to_delete: Optional[List[IdType]] = None
    ):
        """
        Tests fetching a particular ID type
        :param name: The name of the metadata directory
        :param id_type: The type of ID to fetch
        :param expected_id: The expected ID
        :param to_delete: Additional IDs to delete before fetching
        :return: None
        """
        if to_delete is None:
            to_delete = []
        to_delete.append(id_type)

        path = self.get(name)
        meta = Directory(path).metadata

        ids = meta.ids
        self.assertEqual(ids[id_type], [expected_id])
        for item in to_delete:
            ids[item] = []
        meta.ids = ids
        meta.write()

        meta = Directory(path).metadata
        self.assertEqual(meta.ids[id_type], [])

        self.execute_command(["id-fetch", path], [])
        meta = Directory(path).metadata
        self.assertEqual(meta.ids[id_type], [expected_id])

    def test_fetching_imdb_id_using_tvdb(self):
        """
        Tests fetching IMDB IDs using tvdb ids
        :return: None
        """
        self.execute_id_fetch_check(
            "Over the Garden Wall",
            IdType.IMDB,
            "tt3718778"
        )

    def test_fetching_anilist_id_using_myanimelist(self):
        """
        Tests fetching anilist IDs based on myanimelist IDs
        :return: None
        """
        self.execute_id_fetch_check(
            "Fullmetal Alchemist",
            IdType.ANILIST,
            "121"
        )

    def test_fetching_anilist_and_myanimelist_id_using_mangadex(self):
        """
        Tests fetching anilist and myanimelist IDs using mangadex IDs
        :return: None
        """
        for id_type, expected in [
            (IdType.ANILIST, "96754"),
            (IdType.MYANIMELIST, "96044")
        ]:
            self.execute_id_fetch_check(
                "Taishou Otome Otogibanashi",
                id_type,
                expected,
                [IdType.ANILIST, IdType.MYANIMELIST]
            )

    def test_fetching_ids_for_seasons(self):
        """
        Tests fetching IDs for seasons
        :return: None
        """
        path = self.get("Fullmetal Alchemist")
        meta = Tv(path)

        ids = meta.ids
        self.assertEqual(ids[IdType.ANILIST], ["121"])
        ids[IdType.ANILIST] = []

        seasons = meta.seasons
        season = seasons.pop(1)
        self.assertEqual(
            season.name,
            "Fullmetal Alchemist - Reflections"
        )
        season_ids = season.ids
        self.assertEqual(season_ids[IdType.ANILIST], ["664"])
        season_ids[IdType.ANILIST] = []
        season.ids = season_ids
        seasons.insert(1, season)

        meta.ids = ids
        meta.seasons = seasons
        meta.write()

        self.assertEqual(meta.ids[IdType.ANILIST], [])
        self.assertEqual(meta.seasons[1].ids[IdType.ANILIST], [])

        self.execute_command(["id-fetch", path], [])

        meta = Tv(path)

        self.assertEqual(meta.ids[IdType.ANILIST], ["121"])
        self.assertEqual(meta.seasons[1].ids[IdType.ANILIST], ["664"])
