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

from unittest.mock import patch
from toktokkie.metadata.music.Music import Music
from toktokkie.metadata.music.components.MusicSong import MusicSong
from toktokkie.test.TestFramework import _TestFramework


class TestMusicSong(_TestFramework):
    """
    Class that tests the MusicSong class
    """

    def generate_song(self, index: int = 3) -> MusicSong:
        """
        Creates a MusicSong object
        :param index: The index of the song in the album
        :return: None
        """
        aimer = Music(self.get("Aimer"))
        album = aimer.non_theme_song_albums[0]
        return album.songs[index]

    def test_attributes(self):
        """
        Tests the various attributes of the MusicSong class
        :return: None
        """
        song = self.generate_song()

        self.assertEqual(song.title, "d")
        song.title = "ABC"
        self.assertEqual(song.title, "ABC")

        self.assertEqual(song.artist_name, "Aimer")
        song.artist_name = "Hello"
        self.assertEqual(song.artist_name, "Hello")

        self.assertEqual(song.album_artist_name, "Aimer")
        song.album_artist_name = "Hi!"
        self.assertEqual(song.album_artist_name, "Hi!")

        self.assertEqual(song.album_name, "Sleepless Nights")
        song.album_name = "Lazy Days"
        self.assertEqual(song.album_name, "Lazy Days")

        self.assertEqual(song.genre, "J-Pop")
        song.genre = "Anime"
        self.assertEqual(song.genre, "Anime")

        self.assertEqual(song.tracknumber, (4, 4))
        song.tracknumber = (5, 10)
        self.assertEqual(song.tracknumber, (5, 10))
        song._tags.pop("tracknumber")
        self.assertEqual(song.tracknumber, (4, 4))
        song._tags["tracknumber"] = "3"
        self.assertEqual(song.tracknumber, (3, 4))
        song._tags.pop("tracknumber")
        song.path = "A"
        self.assertEqual(song.tracknumber, (1, 4))

        self.assertEqual(song.year, 2012)
        song.year = 2020
        self.assertEqual(song.year, 2020)

    def test_writing_and_reading_mp3_tags(self):
        """
        Tests reading and writing mp3 tags
        :return: None
        """
        song = self.generate_song()
        song.year = 1900
        song.save_tags()
        song = self.generate_song()
        self.assertEqual(song.year, 1900)

    def test_non_mp3(self):
        """
        Tests how non-mp3 songs are handled
        :return: None
        """
        song = self.generate_song(2)
        song.year = 1900
        song.save_tags()
        song = self.generate_song()
        self.assertNotEqual(song.year, 1900)

    def test_removing_tag(self):
        """
        Tests removing a tag
        :return: None
        """
        song = self.generate_song()
        self.assertEqual(song.year, 2012)
        song.year = 1900
        song.save_tags()
        song = self.generate_song()
        self.assertEqual(song.year, 1900)
        song.year = ""
        song._tags["abc"] = ""
        song.save_tags()
        song = self.generate_song()
        self.assertEqual(song.year, 2012)

    def test_mp3_loading(self):
        """
        tests loading from an mp3 file
        :return: None
        """
        class DummyMp3Reader:
            def __init__(self, _):
                self.a = 1

            def __iter__(self):
                yield "date", ["1000"]
                yield "genre", "100",
                yield "album", []

        with patch(
                "toktokkie.metadata.music.components.MusicSong.EasyID3",
                DummyMp3Reader
        ):
            song = self.generate_song()
            self.assertEqual(song.year, 1000)
            self.assertEqual(song.genre, "100")
            self.assertEqual(song.album_name, "")
