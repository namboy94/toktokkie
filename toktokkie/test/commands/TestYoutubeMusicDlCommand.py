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
from toktokkie.enums import IdType
from toktokkie.metadata.music.Music import Music
from toktokkie.test.TestFramework import _TestFramework


class TestYoutubeDlCommand(_TestFramework):
    """
    Class that tests the youtube-music-dl command
    """

    empty_url = "https://www.youtube.com/watch?v=YpfSq487XWM"
    empty_2_url = "https://www.youtube.com/watch?v=ns3fB82nYl0"
    empty_3_url = "https://www.youtube.com/watch?v=3MtYLaRzBu8"
    empty_playlist_url = "https://www.youtube.com/playlist" \
                         "?list=PL5oBP8UuyjH60e6Y5lusXZ8uGEVnQtdGm"

    def test_downloading_song(self):
        """
        Tests downloading a song using youtube-dl
        :return: None
        """
        path = self.get("Tester")
        self.execute_command(
            ["youtube-music-dl", path, "2020", "test", self.empty_url],
            [
                "", "0",  # Create new directory
                "TestVid"
            ]
        )
        meta = Music(path)
        self.assertEqual(len(meta.albums), 1)
        album = meta.albums[0]
        video = os.path.join(album.path, "TestVid-video.mp4")
        audio = os.path.join(album.path, "TestVid.mp3")
        self.assertTrue(os.path.isfile(video))
        self.assertTrue(os.path.isfile(audio))
        self.assertEqual(album.ids[IdType.YOUTUBE_VIDEO], ["YpfSq487XWM"])

    def test_downloading_multiple_songs(self):
        """
        Tests downloading multiple songs
        :return: None
        """
        path = self.get("Tester")
        self.execute_command(
            [
                "youtube-music-dl", path, "2020", "test",
                self.empty_url, self.empty_2_url
            ],
            ["", "0", "TestVid", "OtherVid"]
        )
        meta = Music(path)
        testvid = meta.albums[0]
        othervid = meta.albums[1]
        self.assertEqual(testvid.name, "TestVid")
        self.assertEqual(othervid.name, "OtherVid")
        for album in [testvid, othervid]:
            self.assertTrue(os.path.isfile(os.path.join(
                album.path, f"{album.name}-video.mp4"
            )))
            self.assertTrue(os.path.isfile(os.path.join(
                album.path, f"{album.name}.mp3"
            )))
        self.assertEqual(testvid.ids[IdType.YOUTUBE_VIDEO], ["YpfSq487XWM"])
        self.assertEqual(othervid.ids[IdType.YOUTUBE_VIDEO], ["ns3fB82nYl0"])

    def test_downloading_playlist_album(self):
        """
        Tests downloading a playlist and storing it as its own album
        :return: None
        """
        path = self.get("Tester")
        self.execute_command(
            [
                "youtube-music-dl", path, "2020", "test",
                self.empty_playlist_url,
                "--album-name", "Hello World"
            ],
            ["", "0", "Second", "First", "2"],
        )
        meta = Music(path)
        album = meta.albums[-1]
        self.assertEqual(album.name, "Hello World")
        self.assertEqual(len(album.songs), 2)
        self.assertEqual(len(album.videos), 2)
        self.assertTrue(os.path.isfile(os.path.join(
            album.path, f"01 - First.mp3"
        )))
        self.assertTrue(os.path.isfile(os.path.join(
            album.path, f"02 - Second.mp3"
        )))
        self.assertEqual(
            album.ids[IdType.YOUTUBE_VIDEO], ["ns3fB82nYl0", "3MtYLaRzBu8"]
        )

    def test_music_only(self):
        """
        Tests downloading music only
        :return: None
        """
        path = self.get("Tester")
        self.execute_command(
            [
                "youtube-music-dl", path, "2020", "test",
                self.empty_url, "--only-audio"
            ],
            ["", "0", "TestVid"]
        )
        meta = Music(path)
        album = meta.albums[0]
        video = os.path.join(album.path, "TestVid-video.mp4")
        audio = os.path.join(album.path, "TestVid.mp3")
        self.assertFalse(os.path.isfile(video))
        self.assertTrue(os.path.isfile(audio))

    def test_repeated_download(self):
        """
        Tests if repeated downloads of an album doesn't break existing
        files.
        :return: None
        """
        path = self.get("Tester")
        self.execute_command(
            ["youtube-music-dl", path, "2020", "test", self.empty_url],
            ["", "0", "TestVid"]
        )
        self.execute_command(
            ["youtube-music-dl", path, "2020", "test", self.empty_url],
            ["TestVid"]
        )
        self.execute_command(
            [
                "youtube-music-dl", path, "2020", "test", self.empty_url,
                "--album-name", "ABC"
            ],
            ["", "0", "TestVid"]
        )
        self.execute_command(
            [
                "youtube-music-dl", path, "2020", "test", self.empty_url,
                "--album-name", "ABC"
            ],
            ["", "0", "TestVid"]
        )
        meta = Music(path)
        self.assertEqual(len(meta.albums), 2)

    def test_invalid_metadata(self):
        """
        Tests if invalid metadata is caught correctly
        :return: None
        """
        path = self.get("Over the Garden Wall")
        self.execute_command(
            ["youtube-music-dl", path, "2020", "test", self.empty_url],
            []
        )
