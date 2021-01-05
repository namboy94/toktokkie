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

import tvdb_api
from typing import Dict, Union, List, Tuple


def load_tvdb_series_info(tvdb_id: Union[str, int]) \
        -> Dict[str, Union[str, List[Tuple[str, str]]]]:
    """
    Loads TVDB data.
    :return: None
    """
    tvdb_data = tvdb_api.Tvdb()[int(tvdb_id)]

    episodes = 0
    for season_number in tvdb_data:
        episodes += len(tvdb_data[season_number])

    return {
        "seasons": str(len(tvdb_data)),
        "episodes": str(episodes),
        "status": tvdb_data.data["status"],
        "first_aired": tvdb_data.data["firstAired"],
        "network": tvdb_data.data["network"],
        "runtime": tvdb_data.data["runtime"],
        "genres": ", ".join(tvdb_data.data["genre"]),
        "rating": tvdb_data.data["rating"],
        "synopsys": tvdb_data.data["overview"],
        "order": [
            ("seasons", "Seasons"),
            ("episodes", "Episodes"),
            ("status", "Status"),
            ("first_aired", "First Aired"),
            ("network", "Network"),
            ("runtime", "Runtime"),
            ("genres", "Genres"),
            ("rating", "Rating")
        ]
    }
