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
import requests
from typing import Dict, Any
from toktokkie.verification.lib.anilist.AnilistDate import AnilistDate
from toktokkie.verification.lib.anilist.AnilistRelation import AnilistRelation
from toktokkie.verification.lib.anilist.AnilistEntry import AnilistEntry
from toktokkie.verification.lib.anilist.enums import WatchingState, \
    AiringState, RelationType


class AnilistHandler:
    """
    Class that handles anilist.co API calls
    """

    entries = {}
    """
    The anime entries mapped to their myanimelist IDs
    """

    def __init__(self, username: str):
        """
        Initializes the handler. Fetches all of a user's list entries.
        :param username: The user for which to fetch the entries
        """
        self.username = username
        self.fill_entries()

    def fetch_data(self) -> Dict[str, Any]:
        """
        Fetches the relevant list entry data from the anilist API
        :return: The retrieved data
        """
        query = """
            query ($user: String) {
                MediaListCollection (userName: $user, type: ANIME) {
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
                                idMal
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

    def fill_entries(self):
        """
        Parses the retrieved data and generates list entries, then maps
        them to their myanimelist IDs in a dictionary
        :return: None
        """

        for collection in self.fetch_data()["MediaListCollection"]["lists"]:
            for entry in collection["entries"]:

                start = entry["startedAt"]
                start_date = \
                    AnilistDate(start["year"], start["month"], start["day"])
                end = entry["completedAt"]
                end_date = AnilistDate(end["year"], end["month"], end["day"])

                relations = []
                for relation in entry["media"]["relations"]["edges"]:
                    relations.append(AnilistRelation(
                        entry["idMal"],
                        relation["node"]["idMal"],
                        RelationType[relation["relationType"]]
                    ))
                self.entries[entry["idMal"]] = AnilistEntry(
                    entry["idMal"],
                    self.username,
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
        return json.loads(response.text)
