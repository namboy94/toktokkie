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
from toktokkie.utils.update import updaters, perform_update


class UpdateCommand(Command):
    """
    Class that encapsulates behaviour of the update command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "update"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)

        parser.add_argument("--dry-run", action="store_true",
                            help="Does not download or rename anything")

        # xdcc
        parser.add_argument("--create", action="store_true",
                            help="If this flag is set, "
                                 "will generate new update instructions")
        parser.add_argument("-t", "--throttle", default=-1,
                            help="Limits the download speed of xdcc-dl. "
                                 "Append K,M or G for more convenient units")
        parser.add_argument("--timeout", default=120, type=int,
                            help="Sets a timeout for starting "
                                 "the xdcc-dl download")

        # manga
        parser.add_argument("--no-check-newest-chapter-length",
                            action="store_true",
                            help="Deactivates checking the latest manga "
                                 "chapter for completeness")
        parser.add_argument("--skip-special", action="store_true",
                            help="Skips updating special manga chapters")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        for directory in Directory.load_directories(self.args.directories):

            metadata = directory.metadata
            args = {
                "dry_run": False,
                "create": False,
                "throttle": -1,
                "timeout": 120,
                "no_check_newest_chapter_length": False,
                "skip_special": False
            }
            args.update(dict(self.args.__dict__))

            applicable_updaters = [
                x for x in updaters
                if metadata.media_type() in x.applicable_media_types()
            ]
            perform_update(args, metadata, applicable_updaters)
