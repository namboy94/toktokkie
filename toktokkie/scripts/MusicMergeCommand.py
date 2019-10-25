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
from toktokkie.scripts.Command import Command
from toktokkie.metadata.MediaType import MediaType
from toktokkie.Directory import Directory
from toktokkie.exceptions import MissingMetadata
from toktokkie.metadata.types.MusicArtist import MusicArtist
from puffotter.os import listdir


class MusicMergeCommand(Command):
    """
    Class that encapsulates behaviour of the music-merge command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "music-merge"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        parser.add_argument("source",
                            help="Directory containing one half of "
                                 "the directories to merge")
        parser.add_argument("dest",
                            help="Directory containing the other half "
                                 "of the directories to merge")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        try:
            Directory(self.args.source)
            source_paths = [self.args.source]
        except MissingMetadata:
            source_paths = list(map(lambda x: x[1], listdir(self.args.source)))

        try:
            Directory(self.args.dest)
            dest_paths = [self.args.dest]
            dest_is_metadata_dir = True
        except MissingMetadata:
            dest_is_metadata_dir = False
            dest_paths = list(map(lambda x: x[1], listdir(self.args.dest)))

        source_artists = self.load_directories(
            source_paths, restrictions=[MediaType.MUSIC_ARTIST]
        )
        dest_artists = self.load_directories(
            dest_paths, restrictions=[MediaType.MUSIC_ARTIST]
        )
        dest_names = [x.metadata.name for x in dest_artists]

        for source_artist in source_artists:
            source_metadata = source_artist.metadata  # type: MusicArtist
            if source_metadata.name not in dest_names:
                if dest_is_metadata_dir:
                    self.logger.warning(
                        "Artist names don't match: {} !+ {}".format(
                            source_artist.path,
                            dest_paths[0]
                        )
                    )
                else:
                    new_path = os.path.join(
                        self.args.dest, source_metadata.name
                    )
                    os.rename(source_artist.path, new_path)
            else:
                dest_artist = list(filter(
                    lambda x: source_metadata.name == x.metadata.name,
                    dest_artists
                ))[0]
                dest_metadata = dest_artist.metadata  # type: MusicArtist
                dest_album_names = [x.name for x in dest_metadata.albums]

                for source_album in source_metadata.albums:
                    if source_album.name in dest_album_names:
                        self.logger.warning(
                            "Duplicate album: {}".format(source_album.name)
                        )
                    else:
                        os.rename(
                            os.path.join(
                                source_artist.path, source_album.name
                            ),
                            os.path.join(
                                dest_artist.path, source_album.name
                            )
                        )
                        dest_metadata.add_album(source_album)

                dest_artist.write_metadata()
