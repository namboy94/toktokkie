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
            mal_id: int,
            username: str,
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
        :param mal_id: The myanimelist.net entry
        :param username: The username of the user providing
                         the user-specific data
        :param watching_status: The watching status of the user
        :param airing_status: The airing status of the show
        :param score: The user's score
        :param progress: The user's progress
        :param episodes: The show's total number of episodes
        :param start_date: The date at which the user started to watch
        :param completion_date: The date at which the user completed the series
        :param relations: A list of relations to other shows
        """
        self.mal_id = mal_id
        self.username = username
        self.watching_status = watching_status
        self.airing_status = airing_status
        self.score = score
        self.progress = progress
        self.episodes = episodes
        self.start_date = start_date
        self.completion_date = completion_date
        self.relations = relations
