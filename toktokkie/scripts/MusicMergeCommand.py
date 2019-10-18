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
from toktokkie.metadata.components.enums import MediaType
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
        source_paths = list(map(lambda x: x[1], listdir(self.args.source)))
        dest_paths = list(map(lambda x: x[1], listdir(self.args.dest)))

        source_artists = self.load_directories(
            source_paths, restrictions=[MediaType.MUSIC_ARTIST]
        )
        dest_artists = self.load_directories(
            dest_paths, restrictions=[MediaType.MUSIC_ARTIST]
        )
        dest_names = [x.metadata.name for x in dest_artists]

        for source_artist in source_artists:
            if source_artist.metadata.name not in dest_names:
                os.rename(
                    source_artist.path,
                    os.path.join(self.args.dest, source_artist.metadata.name)
                )
            else:
                dest_artist = list(filter(
                    lambda x: source_artist.metadata.name == x.metadata.name,
                    dest_artists
                ))[0]
                source_albums = source_artist.metadata.all_albums
                dest_albums = dest_artist.metadata.all_albums
                dest_album_names = [x["name"] for x in dest_albums]

                for source_album in source_albums:
                    name = source_album["name"]

                    if name in dest_album_names:
                        self.logger.warning("Duplicate album: {}".format(name))
                    else:
                        os.rename(
                            os.path.join(source_artist.path, name),
                            os.path.join(dest_artist.path, name)
                        )
                        dest_artist.metadata.add_album(source_album)

                dest_artist.write_metadata()
