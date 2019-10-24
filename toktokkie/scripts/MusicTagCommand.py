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
from mutagen.easyid3 import EasyID3
# noinspection PyProtectedMember
from mutagen.id3 import ID3, APIC, TPE2
from puffotter.os import listdir, get_ext
from toktokkie.scripts.Command import Command
from toktokkie.metadata.MediaType import MediaType
from toktokkie.metadata.types.MusicArtist import MusicArtist


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
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        for directory in self.load_directories(
                self.args.directories, restrictions=[MediaType.MUSIC_ARTIST]
        ):
            music_metadata = directory.metadata  # type: MusicArtist
            for album in music_metadata.albums:
                for song, song_file in listdir(
                        os.path.join(directory.path, album.name)
                ):
                    if get_ext(song) != "mp3":
                        self.logger.info("Not an MP3 file: " + song)
                        continue

                    title = song.rsplit(".", 1)[0]
                    if title.split(" - ", 1)[0].isnumeric():
                        title = title.split(" - ", 1)[1]

                    mp3 = EasyID3(song_file)
                    mp3["title"] = title
                    mp3["artist"] = directory.metadata.name
                    mp3["album"] = album.name
                    mp3["date"] = str(album.year)
                    mp3["genre"] = album.genre
                    mp3.save()

                    cover_file = os.path.join(
                        directory.metadata.icon_directory,
                        album.name + ".png"
                    )

                    if os.path.isfile(cover_file):
                        with open(cover_file, "rb") as f:
                            img = f.read()

                        id3 = ID3(song_file)
                        id3.add(APIC(3, "image/jpeg", 3, "Front cover", img))
                        id3.add(TPE2(encoding=3, text=directory.metadata.name))
                        id3.save()
                    else:
                        self.logger.warning("No cover file for {}"
                                            .format(album.name))
