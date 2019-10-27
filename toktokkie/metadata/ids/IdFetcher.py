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

import logging
import tvdb_api
import musicbrainzngs
from typing import List, Dict, Optional
from toktokkie import version
from toktokkie.metadata.MediaType import MediaType
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.ids.mappings import literature_media_types
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
        if id_type == IdType.TVDB:
            return self.__load_tvdb_ids()
        elif id_type == IdType.ANILIST and IdType.MYANIMELIST in other_ids:
            return self.__load_anilist_ids(other_ids[IdType.MYANIMELIST])
        elif id_type == IdType.MUSICBRAINZ_ARTIST:
            return self.__load_musicbrainz_artist_ids()
        else:
            return None

    def __load_tvdb_ids(self) -> List[str]:
        """
        Retrieves TVDB IDs based on the media name
        :return: THe TVDB IDs
        """
        try:
            return [str(tvdb_api.Tvdb()[self.name].data["id"])]
        except (tvdb_api.tvdb_shownotfound, TypeError):
            return []

    def __load_anilist_ids(self, mal_ids: List[str]) -> List[str]:
        """
        Loads anilist IDs based on myanimelist IDs
        :param mal_ids: THe myanimelist IDs
        :return: The anilist IDs
        """
        self.logger.info("Loading anilist ID from mal IDs {}".format(mal_ids))
        list_type = AnimeListMediaType.ANIME
        if self.media_type in literature_media_types:
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

    def __load_musicbrainz_artist_ids(self) -> List[str]:
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
            return [artist_guess["artist-list"][0]["id"]]
        else:
            return ["0"]
