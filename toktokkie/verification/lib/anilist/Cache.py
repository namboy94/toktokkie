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

from toktokkie.verification.lib.anilist.AnilistHandler import AnilistHandler


class Cache:
    """
    Class that 'caches' the AnilistHandler data for a user
    """

    __handlers = {}
    """
    Maps handlers to usernames
    """

    @staticmethod
    def get_handler_for_user(username: str, refresh: bool = False) \
            -> AnilistHandler:
        """
        Retrieves an anilist handler for the given user.
        If one was requested previously, that one will be used instead
        :param username: The user for which to get an anilist handler
        :param refresh: Forces a refresh
        :return: The anilist handler for this user
        """

        if username not in Cache.__handlers or refresh:
            Cache.__handlers[username] = AnilistHandler(username)
        return Cache.__handlers[username]
