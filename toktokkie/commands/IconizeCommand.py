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
from toktokkie.utils.iconizing.Iconizer import Iconizer


class IconizeCommand(Command):
    """
    Class that encapsulates behaviour of the iconize command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "iconize"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        procedure_names = {x.name for x in Iconizer.all_procedures}

        cls.add_directories_arg(parser)
        parser.add_argument("procedure", choices=procedure_names, nargs="?",
                            default=Iconizer.default_procedure().name,
                            help="The procedure to use")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        procedure = list(filter(
            lambda x: x.name == self.args.procedure, Iconizer.all_procedures
        ))[0]

        for directory in Directory.load_directories(self.args.directories):
            iconizer = Iconizer(directory.metadata, procedure)
            iconizer.iconize()