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
from puffotter.os import listdir, get_ext
from toktokkie.commands.Command import Command
from toktokkie.Directory import Directory


class PlaylistCreateCommand(Command):
    """
    Class that encapsulates behaviour of the playlist-create command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "playlist-create"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)
        parser.add_argument("playlist_file",
                            help="The destination playlist file")
        parser.add_argument("--format", choices={"m3u"}, default="m3u",
                            help="The playlist format")
        parser.add_argument("--prefix", help="Prefix for the generated paths")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        music_exts = ["mp3", "flac", "wav", "aac"]

        playlist_files = []

        for directory in Directory.load_directories(self.args.directories):
            for album, album_path in listdir(directory.path, no_files=True):
                for song, song_path in listdir(album_path, no_dirs=True):
                    if get_ext(song) in music_exts:

                        if self.args.prefix is None:
                            playlist_files.append(song_path)
                        else:
                            playlist_files.append(
                                os.path.join(self.args.prefix, song_path)
                            )

        if self.args.format == "m3u":
            playlist = "\n".join(playlist_files)
        else:
            playlist = ""

        with open(self.args.playlist_file, "w") as f:
            f.write(playlist)
