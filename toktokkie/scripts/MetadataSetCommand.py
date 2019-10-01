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

import argparse
from toktokkie.scripts.Command import Command
from toktokkie.metadata.components.enums import IdType


class MetadataSetCommand(Command):
    """
    Class that encapsulates behaviour of the metadata-set command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "metadata-set"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)

        id_types = [x.value for x in IdType]

        subparser = parser.add_subparsers(
            dest="mode", required=True
        )  # type: ignore

        multi_episode_parser = subparser.add_parser(
            "multi-episode", help="Add a multi-episode to a TV Series"
        )
        multi_episode_parser.add_argument("id_type", choices=id_types,
                                          help="The ID type")
        multi_episode_parser.add_argument("season", type=int,
                                          help="The season of the episode")
        multi_episode_parser.add_argument("start_episode", type=int,
                                          help="The start episode")
        multi_episode_parser.add_argument("end_episode", type=int,
                                          help="The end episode")

        exclude_parser = subparser.add_parser(
            "exclude", help="Add an excluded episode to a TV Series"
        )
        exclude_parser.add_argument("id_type", choices=id_types,
                                    help="The ID type")
        exclude_parser.add_argument("season", type=int,
                                    help="The season of the episode")
        exclude_parser.add_argument("episode", type=int,
                                    help="The episode to exclude")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        pass
