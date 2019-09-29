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
import shutil
from toktokkie.scripts.Command import Command
from puffotter.os import makedirs


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

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        output_path = self.args.out

        if output_path is not None:
            makedirs(output_path)

        for directory in self.load_directories(self.args.directories):
            if output_path is None:
                archive_path = directory.path + ".archive"
            else:
                archive_path = os.path.join(
                    output_path, directory.metadata.name
                )
            if not os.path.isdir(archive_path):
                os.makedirs(archive_path)
            self.archive(directory.path, archive_path)

    @staticmethod
    def archive(source: str, dest: str):
        """
        Creates a low-filesize archive of a directory into a new directory
        :param source: The source directory
        :param dest: The destination directory
        :return: None
        """
        for child in os.listdir(source):
            child_path = os.path.join(source, child)
            dest_child_path = os.path.join(dest, child)

            if os.path.isfile(child_path):
                if not child_path.endswith(".json") and \
                        not child_path.endswith(".png"):
                    with open(dest_child_path, "w") as f:
                        f.write("")
                else:
                    shutil.copyfile(child_path, dest_child_path)

            elif os.path.isdir(child_path):
                if not os.path.isdir(dest_child_path):
                    os.makedirs(dest_child_path)

                ArchiveCommand.archive(child_path, dest_child_path)