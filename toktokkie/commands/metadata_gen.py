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
from toktokkie.Directory import Directory
from toktokkie.enums import MediaType
from toktokkie.commands.Command import Command
from toktokkie.exceptions import InvalidDirectoryState


class MetadataGenCommand(Command):
    """
    Class that encapsulates behaviour of the metadata-gen command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "metadata-gen"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Creates new metadata configuration for a directory"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        # noinspection PyTypeChecker
        media_types = list(map(lambda x: x.value, list(MediaType)))
        parser.add_argument("media_type", choices=set(media_types),
                            help="The media type of the metadata")
        cls.add_directories_arg(parser)

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        for directory in self.args.directories:

            try:
                generated = Directory.prompt(
                    directory,
                    self.args.media_type
                ).metadata
                generated.print_folder_icon_source()
            except InvalidDirectoryState as e:
                self.logger.warning(f"Invalid state for directory {directory}:"
                                    f" {e}")
