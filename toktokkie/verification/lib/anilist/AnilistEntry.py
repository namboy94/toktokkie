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

from typing import List
from toktokkie.verification.lib.anilist.enums import WatchingState, AiringState
from toktokkie.verification.lib.anilist.AnilistRelation import AnilistRelation
from toktokkie.verification.lib.anilist.AnilistDate import AnilistDate


class AnilistEntry:
    """
    Class that models an anilist.co entry.
    """

    def __init__(
            self,
            anilist_id: int,
            mal_id: int,
            username: str,
            title: str,
            watching_status: WatchingState,
            airing_status: AiringState,
            score: float,
            progress: int,
            episodes: int,
            start_date: AnilistDate,
            completion_date: AnilistDate,
            relations: List[AnilistRelation]
    ):
        """
        Initializes the entry
        :param anilist_id: The anilist.co ID of this entry
        :param mal_id: The myanimelist.net entry
        :param username: The username of the user providing
                         the user-specific data
        :param title: The title of this series
        :param watching_status: The watching status of the user
        :param airing_status: The airing status of the show
        :param score: The user's score
        :param progress: The user's progress
        :param episodes: The show's total number of episodes
        :param start_date: The date at which the user started to watch
        :param completion_date: The date at which the user completed the series
        :param relations: A list of relations to other shows
        """
        self.anilist_id = anilist_id
        self.mal_id = mal_id
        self.username = username
        self.title = title
        self.watching_status = watching_status
        self.airing_status = airing_status
        self.score = score
        self.progress = progress
        self.episodes = episodes
        self.start_date = start_date
        self.completion_date = completion_date
        self.relations = relations

    def has_valid_date_entries(self) -> bool:
        """
        Checks if the entry has valid date entries
        :return: True if the date entries are valid, False otherwise
        """

        if self.watching_status == WatchingState.COMPLETED:
            return self.start_date.valid() and self.completion_date.valid()
        elif self.watching_status in [
            WatchingState.CURRENT, WatchingState.DROPPED
        ]:
            return self.start_date.valid() and not self.completion_date.valid()
        else:
            return not self.start_date.valid() and \
                   not self.completion_date.valid()

    def get_relation_edges(self, important: bool = True) \
            -> List[AnilistRelation]:
        """
        Retrieves the relations of the entry, optionally filtered
        by important. Important relations are relations that are neither
        an adaptation, a character relation or an alternative relation
        :param important: Specifies if only important relations
                          should be retrieved
        :return: The list of relations
        """
        return list(filter(
            lambda x: x.is_important() or not important,
            self.relations
        ))
