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
from toktokkie.metadata.AnimeSeries import AnimeSeries
from toktokkie.metadata.AnimeMovie import AnimeMovie
from toktokkie.verification.lib.anilist.Cache import Cache
from toktokkie.verification.Verificator import AnilistVerificator


class EntriesInAnilistVerificator(AnilistVerificator):
    """
    Verificator that checks that all local metadata entries are entered
    on anilist.co
    """

    applicable_metadata_types = [AnimeMovie, AnimeSeries]
    """
    Applicable to both anime movies and anime series
    """

    def verify(self) -> bool:
        """
        Checks if all myanimelist IDs are entered on anilist.co
        :return: True if all entries are entered, False otherwise
        """
        return len(self.__get_missing_ids()) <= 0

    def fix(self):
        """
        Attempts to fix the missing ID issue by prompting the user to
        update their anilist.co list.
        :return: None
        """
        self.print_err("Entries missing on anilist.co:")
        for missing in self.__get_missing_ids():
            anilist_id = self.handler.get_anilist_id(missing)
            if anilist_id is None:
                self.print_inf("ID " + str(missing) +
                               " does not exist on anilist.co's database ")
            else:
                self.print_ins("Enter the following entry to your anilist.co "
                               "list:   https://anilist.co/anime/"
                               + str(anilist_id))
                prompt = False
                while prompt or not self.verify():

                    if prompt:
                        self.print_err("No it's hasn't.")

                    prompt = self.prompt("Has the entry been added?")
                    if prompt:
                        self.handler = \
                            Cache.get_handler_for_user(self.username, True)
                        self.entries = self.handler.entries

    def __get_missing_ids(self) -> Set[int]:
        """
        Checks that all myanimelist IDs in the metadata is entered into the
        anilist list.
        :return: A set of myanimelist IDs that could not be found
        """
        return set(filter(
            lambda x: x not in self.entries,
            self.__get_mal_ids()
        ))

    def __get_mal_ids(self) -> Set[int]:
        """
        Retrieves all myanimelist IDs in the metadata
        :return: A set containing all myanimelist IDs in the metadata
        """

        ids = []

        if self.directory.metadata.type == "anime_series":
            for season in self.directory.metadata.seasons.list:
                ids += season.mal_ids.to_json()

        elif self.directory.metadata.type == "anime_movie":
            ids.append(self.directory.metadata.mal_id.to_json())

        else:  # pragma: no cover
            pass

        return set(ids)
