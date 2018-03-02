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
import sys
from typing import Type
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.renaming.schemes.Scheme import Scheme
from toktokkie.renaming.agents.Agent import Agent
from toktokkie.xdcc_update.UpdateInstructions import UpdateInstructions
from toktokkie.exceptions import MissingUpdateInstructionsException


class XDCCUpdater:
    """
    Class that handles XDCC updates
    """

    def __init__(self, path: str, metadata: TvSeries,
                 scheme: Type[Scheme], agent: Type[Agent],
                 create: bool = False):
        """
        Initializes the XDCCUpdater
        :param path: The path to the directory to update
        :param metadata: The metadata of the directory
        :param scheme: The naming scheme to use
        :param agent: The agent to use
        :param create: If set to True, will prompt user to create new
                       xdcc-update instructions
        """
        self.path = path
        self.metadata = metadata
        self.scheme = scheme
        self.agent = agent

        self.update_instructions_file = \
            os.path.join(path, ".meta", "xdcc-update.json")

        if create:

            if os.path.isfile(self.update_instructions_file):
                if input("File exists. Overwrite? (y/n)") != "y":
                    print("Aborted")
                    sys.exit(1)

            self.update_instructions = \
                UpdateInstructions.generate_from_prompts(path)
            self.update_instructions.write(self.update_instructions_file)

        elif not os.path.isfile(self.update_instructions_file):
            raise MissingUpdateInstructionsException()

        else:
            self.update_instructions = \
                UpdateInstructions.from_json_file(self.update_instructions_file)

    def update(self):
        """
        Starts the XDCC Update procedure
        :return:
        """
