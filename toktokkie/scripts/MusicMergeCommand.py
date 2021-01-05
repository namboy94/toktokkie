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
from typing import List, cast
from toktokkie.scripts.Command import Command
from toktokkie.enums import MediaType
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
        parser.add_argument("target",
                            help="Target directory. If not a toktokkie media"
                                 "directory, will try to merge subfolders")
        parser.add_argument("sources", nargs="+",
                            help="Directores containing directories to merge")
        parser.add_argument("--keep", action="store_true",
                            help="If set, does not delete merged directories")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        try:
            Directory(self.args.target)
            targets = [self.args.target]
            single_artist_mode = True
        except MissingMetadata:
            targets = [x[1] for x in listdir(self.args.target)]
            single_artist_mode = False

        sources = []  # type: List[str]
        for path in self.args.sources:
            try:
                Directory(path)
                sources.append(path)
            except MissingMetadata:
                sources += [x[1] for x in listdir(path)]

        target_artists = Directory.load_directories(
            targets, restrictions=[MediaType.MUSIC_ARTIST]
        )
        source_artists = Directory.load_directories(
            sources, restrictions=[MediaType.MUSIC_ARTIST]
        )

        if single_artist_mode:
            for source in source_artists:
                self.merge_artists(target_artists[0], source)

        else:
            target_map = {x.metadata.name: x for x in target_artists}

            for source_artist in source_artists:
                source_metadata = cast(MusicArtist, source_artist.metadata)

                if source_metadata.name not in target_map:
                    new_path = os.path.join(
                        self.args.target, source_metadata.name
                    )
                    shutil.copytree(source_artist.path, new_path)
                    if not self.args.keep:
                        shutil.rmtree(source_artist.path)

                else:
                    target_artist = \
                        target_map[source_metadata.name]  # type: Directory
                    self.merge_artists(target_artist, source_artist)

    def merge_artists(
            self,
            target_artist: Directory,
            source_artist: Directory
    ):
        """
        Merges two artists
        :param target_artist: The target artist
        :param source_artist: The artist to merge into the target
        :return: None
        """
        source_metadata = cast(MusicArtist, source_artist.metadata)
        target_metadata = cast(MusicArtist, target_artist.metadata)

        target_albums = {x.name: x for x in target_metadata.albums}
        source_themes = {x.name: x for x in source_metadata.theme_songs}

        for source_album in source_metadata.albums:
            if source_album.name in target_albums:
                self.logger.warning(
                    "Duplicate album: {}".format(source_album.name)
                )
            else:
                source_path = os.path.join(
                    source_artist.path, source_album.name
                )
                target_path = os.path.join(
                    target_artist.path, source_album.name
                )
                shutil.copytree(source_path, target_path)
                target_metadata.add_album(source_album)

                theme_song = source_themes.get(source_album.name)
                if theme_song is not None:
                    target_metadata.add_theme_song(theme_song)

        target_metadata.write()
        if not self.args.keep:
            shutil.rmtree(source_artist.path)
