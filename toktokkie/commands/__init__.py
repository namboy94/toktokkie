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

from toktokkie.commands.UrlOpenCommand import UrlOpenCommand
from toktokkie.commands.PrintCommand import PrintCommand
from toktokkie.commands.IconizeCommand import IconizeCommand
from toktokkie.commands.RenameCommand import RenameCommand
from toktokkie.commands.ArchiveCommand import ArchiveCommand
from toktokkie.commands.MangaCreateCommand import MangaCreateCommand
from toktokkie.commands.MetadataGenCommand import MetadataGenCommand
from toktokkie.commands.UpdateCommand import UpdateCommand
from toktokkie.commands.MetadataAddCommand import MetadataAddCommand
from toktokkie.commands.SetComicCoverCommand import SetComicCoverCommand
from toktokkie.commands.SuperCutCommand import SuperCutCommand
from toktokkie.commands.AnimeThemeDlCommand import AnimeThemeDlCommand
from toktokkie.commands.AlbumArtFetchCommand import AlbumArtFetchCommand
from toktokkie.commands.MusicTagCommand import MusicTagCommand
from toktokkie.commands.PlaylistCreateCommand import PlaylistCreateCommand
from toktokkie.commands.MusicMergeCommand import MusicMergeCommand
from toktokkie.commands.IdFetchCommand import IdFetchCommand
from toktokkie.commands.YoutubeMusicDlCommand import YoutubeMusicDlCommand
from toktokkie.commands.MetadataValidateCommand import MetadataValidateCommand

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
    MetadataValidateCommand
]
"""
A list of commands for the toktokkie script
"""
