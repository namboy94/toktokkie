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

from toktokkie.scripts.AnilistOpenCommand import AnilistOpenCommand
from toktokkie.scripts.PrintCommand import PrintCommand
from toktokkie.scripts.IconizeCommand import IconizeCommand
from toktokkie.scripts.RenameCommand import RenameCommand
from toktokkie.scripts.ArchiveCommand import ArchiveCommand
from toktokkie.scripts.CheckCommand import CheckCommand
from toktokkie.scripts.MangaCreateCommand import MangaCreateCommand
from toktokkie.scripts.MetadataGenCommand import MetadataGenCommand
from toktokkie.scripts.UpdateCommand import UpdateCommand
from toktokkie.scripts.MetadataAddCommand import MetadataAddCommand
from toktokkie.scripts.SetMangaCoverCommand import SetMangaCoverCommand
from toktokkie.scripts.SuperCutCommand import SuperCutCommand
from toktokkie.scripts.AnimeThemeDlCommand import AnimeThemeDlCommand
from toktokkie.scripts.AlbumArtFetchCommand import AlbumArtFetchCommand
from toktokkie.scripts.MusicTagCommand import MusicTagCommand
from toktokkie.scripts.PlaylistCreateCommand import PlaylistCreateCommand
from toktokkie.scripts.MusicMergeCommand import MusicMergeCommand

toktokkie_commands = [
    PrintCommand,
    AnilistOpenCommand,
    IconizeCommand,
    RenameCommand,
    ArchiveCommand,
    CheckCommand,
    MangaCreateCommand,
    MetadataGenCommand,
    UpdateCommand,
    MetadataAddCommand,
    SetMangaCoverCommand,
    SuperCutCommand,
    AnimeThemeDlCommand,
    AlbumArtFetchCommand,
    MusicTagCommand,
    MusicMergeCommand,
    PlaylistCreateCommand
]
"""
A list of commands for the toktokkie script
"""

try:
    from toktokkie.scripts.GuiCommand import GuiCommand
    toktokkie_commands.append(GuiCommand)
except ImportError as e:
    pass
