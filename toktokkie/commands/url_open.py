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
from subprocess import call
from toktokkie.Directory import Directory
from toktokkie.commands.Command import Command


class UrlOpenCommand(Command):
    """
    Class that encapsulates behaviour of the urlopen command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "url-open"

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

    def execute(self):
        """
        Executes the command
        :return: None
        """
        directories = Directory.load_directories(self.args.directories)
        for directory in directories:
            metadata = directory.metadata
            all_urls = metadata.urls

            for id_type in metadata.id_prompt_order:
                for url in all_urls.get(id_type, []):
                    print(url)
                    call(["xdg-open", url])
