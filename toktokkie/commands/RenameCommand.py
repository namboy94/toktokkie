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
from toktokkie.commands.Command import Command
from toktokkie.Directory import Directory


class RenameCommand(Command):
    """
    Class that encapsulates behaviour of the rename command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "rename"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Renames directory content based on IDs"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)
        parser.add_argument("--noconfirm", action="store_true",
                            help="Skips the user confirmation step")
        parser.add_argument("--include-title", action="store_true",
                            help="Also renames the title based on ID info")

    def execute(self):
        """
        Executes the command
        :return: None
        """
        for directory in Directory.load_directories(self.args.directories):
            directory.metadata.rename(
                noconfirm=self.args.noconfirm,
                skip_title=not self.args.include_title
            )
