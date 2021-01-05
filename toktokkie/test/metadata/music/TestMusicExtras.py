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

from toktokkie.metadata.music.components.MusicAlbum import MusicAlbum
from toktokkie.metadata.music.components.MusicThemeSong import \
    MusicThemeSong
from toktokkie.metadata.music.Music import Music
from toktokkie.test.TestFramework import _TestFramework


class TestMusicExtras(_TestFramework):
    """
    Class that tests the MusicExtras class
    """

    def test_fetching_albums(self):
        """
        Tests fetching albums for an artist
        :return: None
        """
        amalee = Music(self.get("AmaLee"))
        albums = amalee.albums
        self.assertEqual(len(albums), 10)
        self.assertEqual(albums[0].name, "Nostalgia")

    def test_theme_song_differentiation(self):
        """
        Tests if the theme_songs and non_theme_song_albums attributes work
        correctly
        :return: None
        """
        aimer = Music(self.get("Aimer"))
        albums = aimer.albums
        theme_songs = aimer.theme_songs
        non_theme_songs = aimer.non_theme_song_albums

        self.assertEqual(len(albums), len(theme_songs) + len(non_theme_songs))
        self.assertEqual(theme_songs[0].name, "Brave Shine")
        self.assertEqual(theme_songs[1].name, "Torches")
        self.assertEqual(non_theme_songs[0].name, "Sleepless Nights")

    def test_adding_albums(self):
        """
        Tests adding albums
        :return: None
        """
        amalee = Music(self.get("AmaLee"))
        album = MusicAlbum(
            amalee.directory_path,
            amalee.ids,
            {},
            "New Album!",
            "NEW",
            2020
        )
        self.assertEqual(len(amalee.albums), 10)
        amalee.add_album(album)
        self.assertEqual(len(amalee.albums), 11)
        new_album = amalee.albums[-1]
        self.assertEqual(new_album.name, "New Album!")

        amalee.add_album(album)
        self.assertEqual(len(amalee.albums), 11)

    def test_adding_theme_song(self):
        """
        Tests adding a new theme song
        :return: None
        """
        amalee = Music(self.get("AmaLee"))
        album_1 = MusicAlbum(
            amalee.directory_path,
            amalee.ids,
            {},
            "Theme Song 1",
            "anime",
            2020
        )
        theme_song_1 = MusicThemeSong(
            album_1,
            "Theme Song 1",
            "OP",
            {}
        )
        album_2 = MusicAlbum(
            amalee.directory_path,
            amalee.ids,
            {},
            "Theme Song 2",
            "anime",
            2020
        )
        theme_song_2 = MusicThemeSong(
            album_2,
            "Theme Song 2",
            "OP",
            {}
        )
        self.assertEqual(len(amalee.albums), 10)
        self.assertEqual(len(amalee.theme_songs), 0)
        amalee.add_theme_song(theme_song_1)
        self.assertEqual(len(amalee.albums), 11)
        self.assertEqual(len(amalee.theme_songs), 1)
        amalee.add_theme_song(theme_song_1)
        self.assertEqual(len(amalee.albums), 11)
        self.assertEqual(len(amalee.theme_songs), 1)
        amalee.add_theme_song(theme_song_2)
        self.assertEqual(len(amalee.albums), 12)
        self.assertEqual(len(amalee.theme_songs), 2)
