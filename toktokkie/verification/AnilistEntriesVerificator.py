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

from typing import Set

from anime_list_apis.models.attributes.MediaType import MediaType
from toktokkie.metadata.AnimeSeries import AnimeSeries
from toktokkie.metadata.AnimeMovie import AnimeMovie
from toktokkie.verification.Verificator import AnilistVerificator


class AnilistEntriesVerificator(AnilistVerificator):
    """
    Verificator that checks that all local metadata entries are entered
    on anilist.co
    """

    media_type = MediaType.ANIME
    """
    The media type to check
    """

    applicable_metadata_types = [AnimeMovie, AnimeSeries]
    """
    Applicable to both anime movies and anime series
    """

    def _verify(self) -> bool:
        """
        Checks if all myanimelist IDs are entered on anilist.co
        :return: True if all entries are entered, False otherwise
        """
        return len(self.__get_missing_ids_in_list()) <= 0

    def fix(self):
        """
        Attempts to fix the missing ID issue by prompting the user to
        update their anilist.co list.
        :return: None
        """
        for anilist_id in self.__get_missing_ids_in_list():

            self.prompt_until_verified(
                "Entry missing on anilist.co: " + str(anilist_id),
                "Enter the following entry to your anilist.co list:   "
                "https://anilist.co/anime/" + str(anilist_id),
                "Has the entry been added?",
                "No it's hasn't.",
                lambda: self.api.is_in_list(
                    self.media_type, anilist_id, self.username, True
                )
            )

    def __get_missing_ids_in_list(self) -> Set[int]:
        """
        Returns a set of anilist IDs that are not entered into the
        anilist.co list.
        :return: A set of anilist IDs that could not be found
        """
        anilist_ids = list(map(
            lambda x: self.api.get_anilist_id_from_mal_id(self.media_type, x),
            self._get_mal_ids()
        ))
        no_none = list(filter(
            lambda x: x is not None,
            anilist_ids
        ))
        a = set(filter(
            lambda x: not self.api.is_in_list(
                self.media_type, x, self.username
            ),
            no_none
        ))
        return a


class AnilistAnimeEntriesVerificator(AnilistEntriesVerificator):
    """
    Anilist Entries Verificator for anime
    """
    pass


class AnilistMangaEntriesVerificator(AnilistEntriesVerificator):
    """
    Anilist Entries Verificator for manga
    """

    media_type = MediaType.MANGA
    """
    The media type to check
    """

    applicable_metadata_types = []
    """
    Applicable to both anime movies and anime series
    """
