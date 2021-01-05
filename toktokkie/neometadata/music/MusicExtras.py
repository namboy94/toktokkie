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

from abc import ABC
from typing import List
from toktokkie.neometadata.music.components.MusicAlbum import MusicAlbum
from toktokkie.neometadata.music.components.MusicThemeSong import \
    MusicThemeSong
from toktokkie.neometadata.base.MetadataBase import MetadataBase


class MusicExtras(MetadataBase, ABC):
    """
    Additional methods and attributes for music metadata objects
    """

    @property
    def albums(self) -> List[MusicAlbum]:
        """
        :return: All albums in the metadata, regardless if they're just normal
                 albums or theme songs
        """
        return list(map(
            lambda x: MusicAlbum.from_json(self.directory_path, self.ids, x),
            self.json["albums"]
        ))

    @property
    def theme_songs(self) -> List[MusicThemeSong]:
        """
        :return: All theme songs for this music artist
        """
        album_map = {x.name: x for x in self.albums}

        theme_songs = []
        for theme_song in self.json.get("theme_songs", []):
            name = theme_song["name"]
            album = album_map[name]
            theme_songs.append(MusicThemeSong.from_json(album, theme_song))
        return theme_songs

    @property
    def non_theme_song_albums(self) -> List[MusicAlbum]:
        """
        :return: Any albums that are not also theme songs
        """
        theme_song_names = list(map(lambda x: x.name, self.theme_songs))
        return list(filter(
            lambda x: x.name not in theme_song_names,
            self.albums
        ))

    def add_album(self, album_data: MusicAlbum):
        """
        Adds an album to the metadata
        :param album_data: The album metadata to add
        :return: None
        """
        existing = list(map(lambda x: x.name, self.albums))
        if album_data.name not in existing:
            self.json["albums"].append(album_data.json)

    def add_theme_song(self, theme_song: MusicThemeSong):
        """
        Adds a theme song to the metadata
        :param theme_song: The theme song to add
        :return: None
        """
        existing = list(map(lambda x: x.name, self.theme_songs))
        if theme_song.name not in existing:
            self.add_album(theme_song.album)

            if "theme_songs" not in self.json:
                self.json["theme_songs"] = []

            self.json["theme_songs"].append(theme_song.json)
