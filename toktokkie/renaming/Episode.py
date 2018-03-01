"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

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
"""

import os
from typing import List
from toktokkie.renaming.schemes.Scheme import Scheme
from toktokkie.renaming.agents.Agent import Agent


class Episode:
    """
    Class that models an Episode to rename
    """

    def __init__(self, file_path: str, series_name: str, agent_ids: List[int],
                 season: int, episode: int, scheme: Scheme, agent: Agent):
        """
        Initializes the Episode object
        :param file_path: The path to the file
        :param series_name: The name of the series
        :param agent_ids: The agent IDs
        :param season: The season of this episode
        :param episode: The episode number of this episode
        :param scheme: The naming scheme to use
        :param agent: The agent to use
        """
        self.location = os.path.dirname(file_path)
        self.current = os.path.basename(file_path)

        try:
            self.ext = "." + str(self.current.rsplit(".")[1])
        except IndexError:
            self.ext = ""

        self.season = season
        self.episode = episode

        episode_name = agent.fetch_episode_name(agent_ids, season, episode)

        self.new = scheme.generate_episode_name(
            series_name, season, episode, episode_name
        ) + self.ext

    def rename(self):
        """
        Renames the episode file to the new name
        :return: None
        """
        os.rename(
            os.path.join(self.location, self.current),
            os.path.join(self.location, self.new)
        )
