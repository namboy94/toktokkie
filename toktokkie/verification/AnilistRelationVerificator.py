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

from typing import List, Dict
from toktokkie.verification.lib.anilist.AnilistEntry import AnilistEntry
from toktokkie.verification.lib.anilist.enums import WatchingState
from toktokkie.verification.Verificator import AnilistVerificator


class AnilistRelationVerificator(AnilistVerificator):
    """
    Verificator that makes sure that all related anilist entries are:
      1. Entered into the user's anilist account and completed (if not airing)
      2. Exist in the local metadata
    """

    required_attributes = super().required_attributes.update({
        "ignore_on_hold": {
            "type": bool,
            "help": "Ignores 'on hold' entries during anilist relation checks"
        }
    })

    def _verify(self) -> bool:
        """
        Checks if the media directory has no invalid relations
        :return: True if everything is OK, false otherwise
        """
        local = len(self.__get_missing_local_ids())
        anilist = len(self.__get_incorrect_anilist_entry_ids())
        return local + anilist <= 0

    def fix(self):
        """
        Fixes the previously found issues using user prompts
        :return: None
        """
        local_anilist_ids = list(map(
            lambda x: self.handler.get_anilist_id(x),
            self.__get_missing_local_ids()
        ))

        anilist_anilist_ids = list(map(
            lambda x: self.handler.get_anilist_id(x),
            self.__get_incorrect_anilist_entry_ids()
        ))

        if len(local_anilist_ids) > 0:
            self.prompt_until_verified(
                "IDs missing from local files: " + str(local_anilist_ids),
                "Please add the applicable local files",
                "Were the local files and metadata entries added?",
                "No they weren't.",
                lambda: len(self.__get_missing_local_ids()) <= 0
            )

        if len(anilist_anilist_ids):
            self.prompt_until_verified(
                "IDs missing from anilist account: "
                + str(anilist_anilist_ids),
                "Please add the entries to the anilist account",
                "Were the entries added?",
                "No they weren't"
            )

    def __get_missing_local_ids(self) -> List[int]:
        """
        Retrieves a list of IDs that are related on anilist, but
        are missing in the local files.
        If ignore_on_hold is set to True, entries that are set to 'on hold'
        will be ignored
        :return: The list of missing myanimelist IDs
        """

        related = self.__get_related()
        mal_ids = self._get_mal_ids()
        missing = []

        for mal_id in related:
            if mal_id not in mal_ids:
                entry = self.handler.get_entry(mal_id)
                if self.handler.get_anilist_id(mal_id) is None:
                    continue  # No anilist entry
                elif entry is not None \
                        and entry.watching_status == WatchingState.PAUSED \
                        and self.attributes["ignore_on_hold"]:
                    continue  # Ignore "on hold" entry
                else:
                    missing.append(mal_id)

        return missing

    def __get_incorrect_anilist_entry_ids(self) -> List[int]:
        """
        Retrieves a list of anilist entries that are incorrectly set on
        anilist.co.
        :return: The list of incorrect (myanimelist) IDs
        """
        related = self.__get_related()
        incorrect = []

        for mal_id, entry in related.items():
            if entry is None:
                incorrect.append(mal_id)
            elif entry.watching_status != WatchingState.COMPLETED:
                if entry.watching_status == WatchingState.PAUSED \
                        and self.attributes["ignore_on_hold"]:
                    continue
                else:
                    incorrect.append(mal_id)

        return incorrect

    def __get_related(self) -> Dict[int, AnilistEntry]:
        """
        Retrieves all related anilist entries
        :return: A dictionary mapping myanimelist ids to their anilist entries
        """
        related = {}
        for season in self.directory.metadata.seasons.list:
            for mal_id in season.mal_ids.list:
                related.update(self.handler.get_all_related_entries_of_entry(
                    self.handler.get_entry(mal_id), True
                ))

        for ignored in self.directory.metadata.mal_check_ignores.list:
            if ignored in related:
                related.pop(ignored)

        return related
