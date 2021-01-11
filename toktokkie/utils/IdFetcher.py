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

import json
import logging
import tvdb_api
import requests
import musicbrainzngs
# noinspection PyPackageRequirements
from imdb import IMDb
from typing import List, Dict, Optional, Tuple
from puffotter.graphql import GraphQlClient
from toktokkie import version
from toktokkie.enums import IdType, MediaType
from toktokkie.metadata.base.IdHelper import IdHelper
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.MediaType import MediaType as \
    AnimeListMediaType


class IdFetcher:
    """
    Class that handles fetching ID types using the internet
    """

    logger = logging.getLogger(__name__)
    """
    Logger for this class
    """

    def __init__(self, name: str, media_type: MediaType):
        """
        Initializes the ID fetcher
        :param name: The name of the media
        :param media_type: The media type of the media
        """
        self.name = name
        self.media_type = media_type

    def fetch_ids(
            self,
            id_type: IdType,
            other_ids: Dict[IdType, List[str]]
    ) -> Optional[List[str]]:
        """
        Retrieves any supported IDs based on the media name and/or existing
        IDs.
        :param id_type: The ID Type to fetch
        :param other_ids: Any other known IDs
        :return: The IDs or None if no ID could be determined
        """
        minimized_ids = IdHelper.minimize_ids(other_ids)
        results: Optional[List[str]]
        try:
            if id_type == IdType.TVDB:
                results = self.__load_tvdb_ids(minimized_ids)
            elif id_type == IdType.IMDB:
                results = self.__load_imdb_ids(minimized_ids)
            elif id_type == IdType.ANILIST:
                results = self.__load_anilist_ids(minimized_ids)
            elif id_type == IdType.MYANIMELIST:
                results = self.__load_myanimelist_ids(minimized_ids)
            elif id_type == IdType.MUSICBRAINZ_ARTIST:
                results = self.__load_musicbrainz_ids(minimized_ids)
            else:
                results = None
        except Exception as e:
            self.logger.warning(str(e))
            results = None

        if results is None or len(results) == 0:
            return None
        else:
            return results

    def __load_tvdb_ids(self, _: Dict[IdType, List[str]]) \
            -> Optional[List[str]]:
        """
        Loads TVDB IDs
        :param _: Any additional IDs
        :return: The tvdb IDs, or None if none could be found
        """
        return self.__load_tvdb_ids_from_name()

    def __load_imdb_ids(self, other_ids: Dict[IdType, List[str]]) \
            -> Optional[List[str]]:
        """
        Loads IMDB IDs
        :param other_ids: Any additional IDs
        :return: The imdb IDs, or None if none could be found
        """
        if IdType.TVDB in other_ids:
            return self.__load_imdb_ids_from_tvdb(other_ids[IdType.TVDB])
        else:
            return self.__load_imdb_ids_from_name()

    def __load_anilist_ids(self, other_ids: Dict[IdType, List[str]]) \
            -> Optional[List[str]]:
        """
        Loads Anilist IDs
        :param other_ids: Any additional IDs
        :return: The anilist IDs, or None if none could be found
        """
        if IdType.MYANIMELIST in other_ids:
            return self.__load_anilist_ids_from_mal(
                other_ids[IdType.MYANIMELIST]
            )
        elif IdType.MANGADEX in other_ids:
            return self.__load_anilist_ids_from_mangadex(
                other_ids[IdType.MANGADEX]
            )
        else:
            return None

    def __load_myanimelist_ids(self, other_ids: Dict[IdType, List[str]]) \
            -> Optional[List[str]]:
        """
        Loads myanimelist IDs
        :param other_ids: Any additional IDs
        :return: The myanimelist IDs, or None if none could be found
        """
        if IdType.ANILIST in other_ids:
            return self.__load_mal_ids_from_anilist(
                other_ids[IdType.ANILIST]
            )
        elif IdType.MANGADEX in other_ids:
            return self.__load_mal_ids_from_mangadex(
                other_ids[IdType.MANGADEX]
            )
        else:
            return None

    def __load_musicbrainz_ids(self, _: Dict[IdType, List[str]]) \
            -> Optional[List[str]]:
        """
        Loads musicbrainz IDs
        :param _: Any additional IDs
        :return: The musicbrainz IDs, or None if none could be found
        """
        return self.__load_musicbrainz_artist_ids_from_name()

    def __load_tvdb_ids_from_name(self) -> Optional[List[str]]:
        """
        Retrieves TVDB IDs based on the media name
        :return: THe TVDB IDs
        """
        try:
            return [str(tvdb_api.Tvdb()[self.name].data["id"])]
        except (tvdb_api.tvdb_shownotfound, TypeError):
            return None
        except ValueError:
            self.logger.warning("TVDB API now required API keys")
            return None

    def __load_imdb_ids_from_name(self) -> Optional[List[str]]:
        """
        Retrieves IMDB IDs based on the media name
        :return: The IMDB IDs
        """
        results = IMDb().search_movie(self.name)
        if len(results) == 0:
            return None
        else:
            return ["tt" + str(results[0].getID())]

    def __load_imdb_ids_from_tvdb(self, tvdb_ids: List[str]) -> List[str]:
        """
        Loads IMDB IDs based on tvdb IDs
        :param tvdb_ids: THe TVDB IDs
        :return: THe IMDB IDs
        """
        imdb_ids = []

        for tvdb_id in tvdb_ids:
            try:
                imdb_id = tvdb_api.Tvdb()[int(tvdb_id)].data["imdbId"]
                imdb_ids.append(imdb_id)
            except (tvdb_api.tvdb_shownotfound, TypeError):
                self.logger.warning("Show not found")
            except ValueError:
                self.logger.warning("TVDB API now required API keys")
        return imdb_ids

    def __load_anilist_ids_from_mal(self, mal_ids: List[str]) -> List[str]:
        """
        Loads anilist IDs based on myanimelist IDs
        :param mal_ids: THe myanimelist IDs
        :return: The anilist IDs
        """
        self.logger.info("Loading anilist ID from mal IDs {}".format(mal_ids))
        list_type = AnimeListMediaType.ANIME
        if self.media_type in IdHelper.literature_media_types():
            list_type = AnimeListMediaType.MANGA

        ids = []
        api = AnilistApi()
        for mal_id in mal_ids:
            ids.append(str(
                api.get_anilist_id_from_mal_id(
                    list_type, int(mal_id)
                )
            ))
        return ids

    def __load_anilist_ids_from_mangadex(self, mangadex_ids: List[str]) \
            -> List[str]:
        """
        Loads anilist IDs from mangadex IDs
        :param mangadex_ids: The mangadex IDs
        :return: The anilist IDs
        """
        anilist_ids = []
        for mangadex_id in mangadex_ids:
            _id = self.__load_mangadex_related_ids(mangadex_id)[0]
            anilist_ids.append(_id)
        return [x for x in anilist_ids if x is not None]

    def __load_mal_ids_from_anilist(self, anilist_ids: List[str]) \
            -> List[str]:
        """
        Loads myanimelist IDs from anilist IDs
        :param anilist_ids: The anilist IDs
        :return: The myanimelist IDs
        """
        mal_ids = []
        graphql = GraphQlClient("https://graphql.anilist.co")
        query = """
            query ($id: Int, $media_type: MediaType) {
                Media(id: $id, type: $media_type) {
                    idMal
                }
            }
        """
        media_type = "ANIME"
        if self.media_type in IdHelper.literature_media_types():
            media_type = "MANGA"
        for anilist_id in anilist_ids:
            data = graphql.query(
                query,
                {"id": int(anilist_id), "media_type": media_type}
            )
            mal_id = data["data"]["Media"]["idMal"]
            if mal_id is not None:
                mal_ids.append(str(mal_id))
        return mal_ids

    def __load_mal_ids_from_mangadex(self, mangadex_ids: List[str]) \
            -> List[str]:
        """
        Loads myanimelist IDs from mangadex IDs
        :param mangadex_ids: The mangadex IDs
        :return: The myanimelist IDs
        """
        mal_ids = []
        for mangadex_id in mangadex_ids:
            _id = self.__load_mangadex_related_ids(mangadex_id)[1]
            mal_ids.append(_id)
        return [x for x in mal_ids if x is not None]

    def __load_musicbrainz_artist_ids_from_name(self) -> List[str]:
        """
        Retrieves a musicbrainz ID based on the artist name
        :return: The musicbrainz IDs
        """
        musicbrainzngs.set_useragent(
            "toktokkie media manager",
            version,
            "https://gitlab.namibsun.net/namibsun/python/toktokie"
        )
        artist_guess = musicbrainzngs.search_artists(self.name)
        if artist_guess["artist-count"] > 0:
            name = artist_guess["artist-list"][0]["name"]
            if name == self.name:
                return [artist_guess["artist-list"][0]["id"]]
            else:
                return ["0"]
        else:
            return ["0"]

    @staticmethod
    def __load_mangadex_related_ids(mangadex_id: str) \
            -> Tuple[Optional[str], Optional[str]]:
        """
        Loads IDs related to a mangadex ID
        :param mangadex_id: The mangadex ID
        :return: The anilist ID, the myanimelist ID
        """
        url = f"https://mangadex.org/api/v2/manga/{mangadex_id}"
        response = requests.get(url)
        data = json.loads(response.text)
        anilist_id = data["data"]["links"].get("al")
        myanimelist_id = data["data"]["links"].get("mal")
        return anilist_id, myanimelist_id
