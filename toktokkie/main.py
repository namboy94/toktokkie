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
from puffotter.init import argparse_add_verbosity
from toktokkie.commands.url_open import UrlOpenCommand
from toktokkie.commands.print_cmd import PrintCommand
from toktokkie.commands.iconize import IconizeCommand
from toktokkie.commands.rename import RenameCommand
from toktokkie.commands.archive import ArchiveCommand
from toktokkie.commands.manga_create import MangaCreateCommand
from toktokkie.commands.metadata_gen import MetadataGenCommand
from toktokkie.commands.update import UpdateCommand
from toktokkie.commands.metadata_add import MetadataAddCommand
from toktokkie.commands.set_comic_cover import SetComicCoverCommand
from toktokkie.commands.supercut import SuperCutCommand
from toktokkie.commands.anime_theme_dl import AnimeThemeDlCommand
from toktokkie.commands.album_art_fetch import AlbumArtFetchCommand
from toktokkie.commands.music_tag import MusicTagCommand
from toktokkie.commands.playlist_create import PlaylistCreateCommand
from toktokkie.commands.music_merge import MusicMergeCommand
from toktokkie.commands.id_fetch import IdFetchCommand
from toktokkie.commands.youtube_music_dl import YoutubeMusicDlCommand
from toktokkie.commands.metadata_validate import MetadataValidateCommand
from toktokkie.commands.edit import EditCommand

toktokkie_commands = [
    PrintCommand,
    UrlOpenCommand,
    IconizeCommand,
    RenameCommand,
    ArchiveCommand,
    MangaCreateCommand,
    MetadataGenCommand,
    UpdateCommand,
    MetadataAddCommand,
    SetComicCoverCommand,
    SuperCutCommand,
    AnimeThemeDlCommand,
    AlbumArtFetchCommand,
    MusicTagCommand,
    MusicMergeCommand,
    PlaylistCreateCommand,
    IdFetchCommand,
    YoutubeMusicDlCommand,
    MetadataValidateCommand,
    EditCommand
]
"""
A list of commands for the toktokkie script
"""


def main(args: argparse.Namespace):
    """
    The main function of this script
    :param args: The command line arguments
    :return: None
    """
    for command_cls in toktokkie_commands:
        if command_cls.name() == args.command:
            command = command_cls(args)
            command.execute()


def define_parser() -> argparse.ArgumentParser:
    """
    :return: The command line parser for this script
    """
    parser = argparse.ArgumentParser()
    argparse_add_verbosity(parser)
    command_parser = parser.add_subparsers(dest="command")
    command_parser.required = True

    for command_cls in sorted(toktokkie_commands, key=lambda x: x.name()):
        subparser = command_parser.add_parser(
            command_cls.name(), help=command_cls.help()
        )
        argparse_add_verbosity(subparser)
        command_cls.prepare_parser(subparser)

    return parser
