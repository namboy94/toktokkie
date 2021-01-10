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
from typing import List, Tuple
from puffotter.os import listdir, touch
from toktokkie.metadata.music.Music import Music
from toktokkie.test.TestFramework import _TestFramework


class TestRenamingMusicMetadata(_TestFramework):
    """
    Class that tests the MusicRenamer class
    """

    @staticmethod
    def scramble_music_files(music: Music) -> List[Tuple[str, str]]:
        """
        Scrambles music file names
        :param music: the music metadata
        :return: The old and new file paths
        """
        theme_songs = [x.name for x in music.theme_songs]
        renamed = []
        for album in music.albums:
            for name, path in listdir(album.path, no_dirs=True):
                if album.name in theme_songs:
                    if name.startswith(album.name):
                        continue
                    new_path = os.path.join(album.path, "Z" + name)
                else:
                    new_path = os.path.join(
                        album.path, name.split(" - ", 1)[1]
                    )
                os.rename(path, new_path)
                renamed.append((path, new_path))
        return renamed

    def test_renaming_music(self):
        """
        Tests renaming music
        :return: None
        """
        aimer = Music(self.get("Aimer"))
        renamed = self.scramble_music_files(aimer)

        for old, new in renamed:
            self.assertFalse(os.path.isfile(old))
            self.assertTrue(os.path.isfile(new))

        aimer.rename(noconfirm=True)

        for old, new in renamed:
            self.assertTrue(os.path.isfile(old))
            self.assertFalse(os.path.isfile(new))

        aimer.rename(noconfirm=True)

        for old, new in renamed:
            self.assertTrue(os.path.isfile(old))
            self.assertFalse(os.path.isfile(new))

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        amalee = Music(self.get("AmaLee"))

        correct_files = []
        for album, album_path in listdir(amalee.directory_path):
            for song, song_file in listdir(album_path):
                correct_files.append(song_file)

        amalee.rename(noconfirm=True)

        for correct_file in correct_files:
            self.assertTrue(os.path.isfile(correct_file))

    def test_renaming_single_song(self):
        """
        Tests renaming a single song
        :return: None
        """
        amalee = Music(self.get("AmaLee"))
        first = amalee.albums[0]
        for _, path in listdir(first.path):
            os.remove(path)
        touch(os.path.join(first.path, "abc.mp3"))
        amalee.rename(noconfirm=True)
        self.assertTrue(os.path.isfile(
            os.path.join(first.path, f"{first.name}.mp3")
        ))

    def test_renaming_single_song_with_video(self):
        """
        Tests renaming a single song that includes a video file
        :return: None
        """
        amalee = Music(self.get("AmaLee"))
        first = amalee.albums[0]
        for _, path in listdir(first.path):
            os.remove(path)
        touch(os.path.join(first.path, "abc.mp3"))
        touch(os.path.join(first.path, "abc.mp4"))
        amalee.rename(noconfirm=True)
        self.assertTrue(os.path.isfile(
            os.path.join(first.path, f"{first.name}.mp3")
        ))
        self.assertTrue(os.path.isfile(
            os.path.join(first.path, f"{first.name}-video.mp4")
        ))

    def test_renaming_with_videos(self):
        """
        Tests renaming a regular album with videos
        :return: None
        """
        amalee = Music(self.get("AmaLee"))
        first = amalee.albums[0]
        pre_rename = []
        post_rename = []
        music_files = []
        for song in first.songs:
            wrong = os.path.join(first.path, f"{song.title}.mp4")
            right = os.path.join(
                first.path,
                f"{str(song.tracknumber[0]).zfill(2)} - {song.title}-video.mp4"
            )
            touch(wrong)
            pre_rename.append(wrong)
            post_rename.append(right)
            music_files.append(song.path)

        amalee.rename(noconfirm=True)

        for video_file in pre_rename:
            self.assertFalse(os.path.isfile(video_file))
        for video_file in post_rename:
            self.assertTrue(os.path.isfile(video_file))
        for music_file in music_files:
            self.assertTrue(os.path.isfile(music_file))
