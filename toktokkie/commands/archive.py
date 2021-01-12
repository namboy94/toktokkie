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
from puffotter.prompt import yn_prompt
from toktokkie.commands.Command import Command
from toktokkie.Directory import Directory


class ArchiveCommand(Command):
    """
    Class that encapsulates behaviour of the archive command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "archive"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Archives the folder structure and metadata"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)
        parser.add_argument("--out", "-o", default=None,
                            help="Specifies an output directory for the "
                                 "archived directory/directories")
        parser.add_argument("--keep-icons", action="store_true",
                            help="Keeps original icon files")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        directories = Directory.load_directories(self.args.directories)
        for directory in directories:
            metadata = directory.metadata

            if self.args.out is None:
                archive_path = os.path.basename(directory.path) + ".archive"
            else:
                if len(directories) == 1:
                    archive_path = self.args.out
                else:
                    archive_path = os.path.join(self.args.out, metadata.name)
            if os.path.exists(archive_path):
                if not yn_prompt(f"{archive_path} already exists. Delete it?"):
                    continue

            metadata.archive(archive_path, self.args.keep_icons)
