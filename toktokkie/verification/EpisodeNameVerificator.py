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

from typing import Dict, Any, List
from toktokkie.renaming.export import agents, schemes
from toktokkie.renaming.Renamer import Renamer, Episode
from toktokkie.verification.Verificator import Verificator
from toktokkie.renaming.schemes.Plex import Plex
from toktokkie.renaming.agents.TVDB import TVDB
from toktokkie.metadata.TvSeries import TvSeries


class EpisodeNameVerificator(Verificator):
    """
    Makes sure that all episodes are named correctly
    """

    applicable_metadata_types = [TvSeries]
    """
    Metadata classes on which this verificator may be executed on
    Also applicable to children of those classes
    """

    required_attributes = {
        "naming_scheme": {
            "type": str,
            "help": "The naming scheme to use",
            "default": Plex.name,
            "choices": list(map(lambda x: x.name, schemes))
        },
        "naming_agent": {
            "type": str,
            "help": "The naming agent to use",
            "default": TVDB.name,
            "choices": list(map(lambda x: x.name, agents))
        }
    }
    """
    The required attributes for this verificator
    """

    def __init__(self, directory, attributes: Dict[str, Any]):
        """
        Intializes the Verificator. Automatically creates a renamer object
        from the provided attributes
        :param directory: The directory to verify
        :param attributes: The attributes to use
        """
        super().__init__(directory, attributes)

        scheme_name = self.attributes["naming_scheme"]
        agent_name = self.attributes["naming_agent"]

        self.scheme = list(filter(lambda x: x.name == scheme_name, schemes))[0]
        self.agent = list(filter(lambda x: x.name == agent_name, agents))[0]

    def verify(self) -> bool:
        """
        Checks if all episode names are correct
        :return: True if the names are correct, false otherwise
        """
        invalid_episodes = self.__get_invalid_episodes()
        return len(invalid_episodes) <= 0

    def fix(self):
        """
        Fixes the episode names after a confirmation by the user
        :return: None
        """
        invalid_episodes = self.__get_invalid_episodes()
        self.print_err("Episode Names are incorrect:")

        padding = len(
            max(invalid_episodes, key=lambda x: len(x.current)).current
        ) + 1

        for episode in invalid_episodes:
            self.print_inf(episode.current.ljust(padding) +
                           " !=   " +
                           episode.new)

        self.print_ins("Look over the new episode names "
                       "and initiate the renaming:")

        renamer = Renamer(
            self.directory.path, self.directory.metadata,
            self.scheme, self.agent
        )
        renamer.rename(False)

    def __get_invalid_episodes(self) -> List[Episode]:
        """
        Looks for episodes that have incorrect names.
        :return: A list of episodes with incorrect names
        """
        renamer = Renamer(
            self.directory.path, self.directory.metadata,
            self.scheme, self.agent
        )

        invalid = []
        for episode in renamer.episodes:
            if episode.current != episode.new:
                invalid.append(episode)
        return invalid
