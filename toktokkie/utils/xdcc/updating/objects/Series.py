"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

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
LICENSE
"""

# imports
import os
from typing import List, Dict
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from toktokkie.utils.renaming.objects.TVEpisode import TVEpisode
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager


class Series(object):
    """
    Class that models a Series for the XDCC Updater. It is essentially a light wrapper around a
    dictionary, which can be stored as JSON data
    """

    def __init__(self, destination_directory: str, search_name: str, quality_identifier: str,
                 bot_preference: str, season: int, search_engines: List[str], naming_scheme: str) -> None:

        self.data = {
            "destination_directory": destination_directory,
            "search_name": search_name,
            "quality_identifier": quality_identifier,
            "bot_preference": bot_preference,
            "season": season,
            "search_engines": search_engines,
            "naming_scheme": naming_scheme
        }

    def to_dict(self) -> Dict[str, str or int or List[str]]:
        """
        Turns the data into a dictionary

        :return: The data as dictionary
        """
        return self.data

    def is_same(self, data: Dict[str, str or int or List[str]]) -> bool:
        """
        Checks if this show is equal to another dictionary

        :param data: The data to check
        :return:     true if it is the same, false otherwise
        """
        equal = True
        for key in data:
            if data[key] != self.data[key]:
                equal = False
        return equal

    def update(self) -> None:
        """
        Updates the Series

        :return: None
        """
        MetaDataManager.generate_media_directory(self.data["destination_directory"], media_type="tv_series")
        season_dir = os.path.join(self.data["destination_directory"], "Season " + str(self.data["season"]))

        if not os.path.isdir(season_dir):
            os.makedirs(season_dir)

        self.check_existing_episode_names()
        self.download_new_episodes()

    def check_existing_episode_names(self, season_dir: str) -> None:
        """
        Checks the already existing episodes if they still have the most up-to-date episode names

        :param season_dir: The season directory to check
        :return:           None
        """
        for i, episode in enumerate(sorted(os.listdir(season_dir))):
            episode_file = os.path.join(season_dir, episode)
            tv_episode = TVEpisode(episode_file, i + 1, self.data["season"], self.data["destination_directory"],
                                   SchemeManager.get_scheme_from_scheme_name(self.data["naming_scheme"]))
            tv_episode.rename()

    def download_new_episodes(self, season_dir: str) -> None:
        """
        Downloads new episodes found using the XDCC pack searchers

        :param season_dir: The Season directory in which the files will be stored
        :return:           None
        """
        first_episode_to_check = len(os.listdir(season_dir)) + 1

    def search_for_episode(self, episode: int) -> List[XDCCPack]:
        """
        Searches for a specific episode, and returns the results

        :param episode: The episode to search for
        :return:        A list of found XDCC Packs
        """
        results = []

        search_query = self.data["search_name"] + " " + str(episode).zfill(2)

        search = PackSearcher(self.data["search_engines"]).search(search_query)




            for searcher in search_engines:

                search_engine = SearchEngineManager.get_search_engine_from_string(searcher)

                episode_string = str(episode) if episode >= 10 else "0" + str(episode)

                episode_patterns = [horriblesubs_name + " - " + episode_string + " \[" + quality + "\].mkv",
                                    horriblesubs_name + "_-_" + episode_string]

                results = search_engine(horriblesubs_name + " " + episode_string).search()

                for result in results:
                    for pattern in episode_patterns:
                        if result.bot == bot and re.search(re.compile(pattern), result.filename):
                            return result
            return None