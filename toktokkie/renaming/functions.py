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

import logging
import tvdb_api
from tvdb_api import tvdb_episodenotfound, tvdb_seasonnotfound, \
    tvdb_shownotfound
from typing import Optional
from puffotter.os import get_ext


def generate_tv_episode_filename(
        original_file: str,
        series_name: str,
        season_number: int,
        episode_number: int,
        episode_name: str,
        multi_end: Optional[int] = None
):
    """
    Generates an episode name for a given episode
    :param original_file: The original file. Used to get the file extension
    :param series_name: The name of the series
    :param season_number: The season number
    :param episode_name: The episode name
    :param episode_number: The episode number
    :param multi_end: Can be provided to create a multi-episode range
    :return: The generated episode name
    """
    ext = get_ext(original_file)
    if ext is not None:
        ext = "." + ext
    else:
        ext = ""

    if multi_end is None:
        return "{} - S{}E{} - {}{}".format(
            series_name,
            str(season_number).zfill(2),
            str(episode_number).zfill(2),
            episode_name,
            ext
        )
    else:
        return "{} - S{}E{}-E{} - {}{}".format(
            series_name,
            str(season_number).zfill(2),
            str(episode_number).zfill(2),
            str(multi_end).zfill(2),
            episode_name,
            ext
        )


def load_tvdb_episode_name(
        tvdb_id: str,
        season_number: int,
        episode_number: int,
        multi_end: Optional[int] = None
) -> str:
    """
    Loads an episode name from TVDB
    :param tvdb_id: The TVDB ID for the episode's series
    :param season_number: The season number
    :param episode_number: The episode number
    :param multi_end: If provided,
                      will generate a name for a range of episodes
    :return: The TVDB name
    """
    if int(tvdb_id) == 0:
        return "Episode " + str(episode_number)

    if multi_end is not None:
        episode_names = []
        for episode in range(episode_number, multi_end + 1):
            episode_names.append(load_tvdb_episode_name(
                tvdb_id,
                season_number,
                episode
            ))
        return " | ".join(episode_names)

    try:
        tvdb = tvdb_api.Tvdb()
        info = tvdb[int(tvdb_id)]
        return info[season_number][episode_number]["episodeName"]

    except (tvdb_episodenotfound, tvdb_seasonnotfound, tvdb_shownotfound,
            ConnectionError, KeyError, AttributeError) as e:
        # If not found, or other error, just return generic name
        if str(e) == "cache_location":  # pragma: no cover
            logging.getLogger(__name__).warning("TheTVDB.com is down!")

        return "Episode " + str(episode_number)
