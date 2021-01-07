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
from subprocess import Popen
from toktokkie.Directory import Directory
from toktokkie.commands.Command import Command
from toktokkie.enums import MediaType


class UrlOpenCommand(Command):
    """
    Class that encapsulates behaviour of the urlopen command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "urlopen"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Opens the stored IDs in a browser"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)
        parser.add_argument("--browser", default="firefox",
                            help="The browser to use for opening the URLs")

    def execute(self):
        """
        Executes the command
        :return: None
        """
        # TODO re-implement
        anilist_types = [
            MediaType.COMIC,
            MediaType.BOOK,
            MediaType.BOOK_SERIES,
            MediaType.TV_SERIES,
            MediaType.MOVIE
        ]
        directories = Directory.load_directories(
            self.args.directories, anilist_types
        )
        for directory in directories:
            urls = directory.metadata.get_anilist_urls()
            if len(urls) is None:
                self.logger.warning(
                    "No URL for {}".format(directory.metadata.name)
                )
            else:
                for url in urls:
                    Popen([self.args.browser, url]).wait()
