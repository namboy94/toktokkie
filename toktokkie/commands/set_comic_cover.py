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

import os
import argparse
from subprocess import Popen
from toktokkie.commands.Command import Command
from toktokkie.enums import MediaType
from toktokkie.Directory import Directory


class SetComicCoverCommand(Command):
    """
    Class that encapsulates behaviour of the set-comic-cover command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "set-comic-cover"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Creates a comic cover cbz file"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        for directory in Directory.load_directories(
                self.args.directories, restrictions=[MediaType.COMIC]
        ):

            cover = os.path.join(directory.metadata.icon_directory, "main.png")
            target = os.path.join(directory.path, "cover.cbz")
            if os.path.isfile(cover):
                if not os.path.isfile(target):
                    Popen(["zip", "-j", target, cover]).wait()
            else:
                self.logger.warning("No cover for {}".format(directory.path))