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

import time
import json
import requests
from typing import List, Dict, Any
from toktokkie.verification.lib.anilist.AnilistDate import AnilistDate
from toktokkie.verification.lib.anilist.AnilistRelation import AnilistRelation
from toktokkie.verification.lib.anilist.AnilistEntry import AnilistEntry
from toktokkie.verification.lib.anilist.enums import WatchingState, \
    AiringState, RelationType


class AnilistHandler:
    """
    Class that handles anilist.co API calls
    """

    entries = {}  # type: Dict[int, AnilistEntry]
    """
    The anime entries mapped to their myanimelist IDs
    """

    missing_anilist_ids = []
    """
    Keeps track of myanimelist IDs without a corresponding anilist ID
    """

    def __init__(self, username: str):
        """
        Initializes the handler. Fetches all of a user's list entries.
        :param username: The user for which to fetch the entries
        """
        self.username = username
        self.__fill_entries()

    def get_entry(self, mal_id: int) -> AnilistEntry or None:
        """
        Retrieves an entry from the user's anilist.
        If an entry was not found, return None
        :param mal_id: The myanimelist ID to use
        :return: The entry or None if not found
        """
        if mal_id in self.entries:
            return self.entries[mal_id]
        else:
            return None

    def get_anilist_id(self, mal_id: int or None) -> int or None:
        """
        Retrieves a single anilist ID for an entry
        :param mal_id: The myanimelist ID for which to fetch the anilist ID.
                       If the ID is None, None will also be returned
        :return: The anilist ID, or None if anilist.co does not have an entry
                 for the specified myanimelist ID
        """
        if mal_id in self.missing_anilist_ids:
            return None

        elif mal_id is None:
            return None

        elif mal_id in self.entries:
            return self.entries[mal_id].anilist_id

        else:
            query = """
                query ($mal_id: Int) {
                    Media (idMal: $mal_id) {
                        id
                    }
                }
            """
            data = self.query(query, {"mal_id": mal_id})

            if "errors" in data:
                self.missing_anilist_ids.append(mal_id)
                return None
            else:
                return data["data"]["Media"]["id"]

    def get_all_related_entries_of_entry(
            self,
            entry: AnilistEntry,
            important: bool = True,
            __handled_ids: List[int] = None,
    ) -> Dict[int, AnilistEntry or None]:
        """
        Retrieves all related entries of a list entry.
        Entries that are not in the user's list are replaced by None
        :param entry: The entry for whcih to retrieve the related entries
        :param important: Specifies if only important relations should be
                          retrieved
        :param __handled_ids: Used during recursive calls to fetch ALL
                              relations
        :return: A dictionary mapping the mal IDs to the related entries
        """
        if entry is None:
            return {}

        related_entries = {entry.mal_id: entry}

        handled_ids = [entry.mal_id]
        if __handled_ids is not None:
            handled_ids += __handled_ids

        for relation in entry.get_relation_edges(important):

            if self.get_anilist_id(relation.mal_id) is None:
                continue
            elif relation.mal_id in handled_ids:
                continue
            else:
                inner_entry = self.get_entry(relation.mal_id)

                if inner_entry is None:
                    related_entries[relation.mal_id] = inner_entry
                else:
                    related_entries.update(
                        self.get_all_related_entries_of_entry(
                            inner_entry, important, handled_ids
                        )
                    )

        return related_entries

    def __fetch_data(self) -> Dict[str, Any]:
        """
        Fetches the relevant list entry data from the anilist API
        :return: The retrieved data
        """
        query = """
            query ($username: String) {
                MediaListCollection (userName: $username, type: ANIME) {
                    lists {
                        entries {
                            status
                            score
                            progress
                            startedAt {
                                year
                                month
                                day
                            }
                            completedAt {
                                year
                                month
                                day
                            }
                            media {
                                id
                                idMal
                                title {
                                    userPreferred
                                }
                                status
                                episodes
                                relations {
                                    edges {
                                        node {
                                            idMal
                                        }
                                        relationType
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """
        return self.query(query, {"username": self.username})["data"]

    def __fill_entries(self):
        """
        Parses the retrieved data and generates list entries, then maps
        them to their myanimelist IDs in a dictionary
        :return: None
        """
        for collection in self.__fetch_data()["MediaListCollection"]["lists"]:
            for entry in collection["entries"]:

                if entry["media"]["idMal"] is None:
                    continue

                start = entry["startedAt"]
                start_date = \
                    AnilistDate(start["year"], start["month"], start["day"])
                end = entry["completedAt"]
                end_date = AnilistDate(end["year"], end["month"], end["day"])

                relations = []
                for relation in entry["media"]["relations"]["edges"]:
                    relations.append(AnilistRelation(
                        entry["media"]["idMal"],
                        relation["node"]["idMal"],
                        RelationType[relation["relationType"]]
                    ))
                self.entries[entry["media"]["idMal"]] = AnilistEntry(
                    entry["media"]["id"],
                    entry["media"]["idMal"],
                    self.username,
                    entry["media"]["title"]["userPreferred"],
                    WatchingState[entry["status"]],
                    AiringState[entry["media"]["status"]],
                    entry["score"],
                    entry["progress"],
                    entry["media"]["episodes"],
                    start_date,
                    end_date,
                    relations
                )

    @staticmethod
    def query(query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Queries the Anilist GraphQL API
        :param query: The query to send
        :param variables: The variables to send
        :return: The resulting JSON data
        """
        url = 'https://graphql.anilist.co'
        response = requests.post(
            url, json={'query': query, 'variables': variables}
        )
        time.sleep(0.5)
        return json.loads(response.text)
