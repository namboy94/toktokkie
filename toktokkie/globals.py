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

import os
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.cache.Cache import Cache

"""
Evil global state!
"""


class Globals:
    """
    Class/Singleton containing global state variables
    """

    cache_location = os.path.join(os.path.expanduser("~"), ".toktokkie/cache")
    """
    The location of the cache
    """

    __api_cache = None  # type: Cache
    """
    A global cache for API connections
    """

    __anilist_api = None  # type: AnilistApi
    """
    An Anilist API connection
    """

    @staticmethod
    def get_anilist_api(refresh: bool = False) -> AnilistApi:
        """
        Retrieves an Anilist API connector
        :param refresh: If set to True, generate a new object
        :return: The anilist API connector
        """
        if refresh or Globals.__anilist_api is None:
            Globals.__anilist_api = AnilistApi(
                cache=Globals.get_api_cache(refresh)
            )
        return Globals.__anilist_api

    @staticmethod
    def get_api_cache(refresh: bool = False) -> Cache:
        """
        Retrieves an API Cache
        :param refresh: If set to True, generate a new object
        :return: The API cache
        """
        if refresh or Globals.__api_cache is None:
            Globals.__api_cache = Cache(cache_location=Globals.cache_location)
        return Globals.__api_cache
