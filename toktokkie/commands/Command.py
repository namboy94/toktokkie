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
import logging


class Command:
    """
    Class that encapsulates behaviour of a command for the toktokkie script
    """

    def __init__(self, args: argparse.Namespace):
        """
        Initializes the command object
        :param args: The command line arguments
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.args = args

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        raise NotImplementedError()  # pragma: no cover

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        raise NotImplementedError()  # pragma: no cover

    @staticmethod
    def add_directories_arg(parser: argparse.ArgumentParser):
        """
        Adds a directories argument to a parser
        :param parser: The parser to which to add the argument
        :return: None
        """
        parser.add_argument("directories", nargs="+",
                            help="The directories to use. Files and "
                                 "directories that do not contain a valid "
                                 "metadata configuration will be ignored.")
