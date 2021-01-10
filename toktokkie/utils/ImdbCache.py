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

from typing import Dict, Optional
from imdb import IMDb, IMDbDataAccessError
from imdb.Movie import Movie


class ImdbCache:
    """
    Class that caches IMDB results
    """

    episode_cache: Dict[str, Dict[int, Dict[int, Movie]]] = {}
    """
    The cache for episodes
    Format: {imdb_id: {season: {episode: episode_info}}}
    """

    imdb_api = IMDb()
    """
    The IMDb API object
    """

    @staticmethod
    def load_episode(
            imdb_id: str,
            season: int,
            episode: int
    ) -> Optional[Movie]:
        """
        Loads information about a particular episode for an IMDB ID
        :param imdb_id: The IMDB ID
        :param season: The season
        :param episode: The episode
        """
        if season == 0:
            season = -1

        imdb_id_int = imdb_id.replace("tt", "")
        existing = ImdbCache.episode_cache\
            .get(imdb_id_int, {})\
            .get(season, {})\
            .get(episode)

        if existing is None and imdb_id_int not in ImdbCache.episode_cache:
            ImdbCache.episode_cache[imdb_id_int] = {}

            try:
                data = ImdbCache.imdb_api\
                    .get_movie_episodes(imdb_id_int)["data"]["episodes"]
            except IMDbDataAccessError:
                data = {}
            for _season, episodes in data.items():
                ImdbCache.episode_cache[imdb_id_int][_season] = {}
                for number, _episode in episodes.items():
                    ImdbCache.episode_cache[imdb_id_int][_season][number] \
                        = _episode
            return ImdbCache.load_episode(imdb_id, season, episode)
        else:
            return existing

    @staticmethod
    def load_episode_name(
            imdb_id: str,
            season: int,
            episode: int
    ) -> str:
        """
        Loads a name for an IMDB ID and season/episode
        :param imdb_id: The IMDB ID
        :param season: The season
        :param episode: The episode
        """
        episode_info = ImdbCache.load_episode(imdb_id, season, episode)
        if episode_info is None:
            return f"Episode {episode}"
        else:
            return episode_info["title"]
