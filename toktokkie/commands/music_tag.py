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
from toktokkie.enums import MediaType
from toktokkie.metadata.music.Music import Music


class MusicTagCommand(Command):
    """
    Class that encapsulates behaviour of the music-tag command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "music-tag"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Modifies the mp3 music tags based on metadata"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)
        parser.add_argument("--force-album-art-refresh", action="store_true",
                            help="Forces an album art refresh")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        for directory in Directory.load_directories(
                self.args.directories, restrictions=[MediaType.MUSIC_ARTIST]
        ):
            music_metadata = directory.metadata  # type: Music
            music_metadata.apply_tags(self.args.force_album_art_refresh)
