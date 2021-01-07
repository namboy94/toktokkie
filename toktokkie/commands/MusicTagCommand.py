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
import mutagen.id3
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
            for album in music_metadata.albums:
                for song in album.songs:

                    title = song.filename.rsplit(".", 1)[0]
                    if title.split(" - ", 1)[0].isnumeric():
                        title = title.split(" - ", 1)[1]

                    song.title = title
                    song.artist_name = album.artist_name
                    song.album_artist_name = album.artist_name
                    song.album_name = album.name
                    song.year = album.year
                    song.genre = album.genre

                    song.save_tags()

                    cover_file = os.path.join(
                        directory.metadata.icon_directory,
                        album.name + ".png"
                    )
                    if not os.path.isfile(cover_file):
                        self.logger.warning("No specific cover file for {}"
                                            .format(album.name))
                        cover_file = os.path.join(
                            directory.metadata.icon_directory, "main.png"
                        )

                    if os.path.isfile(cover_file):
                        id3 = mutagen.id3.ID3(song.path)

                        for key in list(id3.keys()):
                            if str(key).startswith("APIC") \
                                    and key != "APIC:Cover":
                                id3.pop(key)

                        if "APIC:Cover" not in id3.keys() or \
                                self.args.force_album_art_refresh:
                            with open(cover_file, "rb") as f:
                                img = f.read()

                            apic = mutagen.id3.APIC(
                                3,
                                "image/jpeg",
                                3,
                                "Cover",
                                img
                            )
                            id3.add(apic)

                        id3.save()
