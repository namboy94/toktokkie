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
