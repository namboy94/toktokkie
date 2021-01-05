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
from unittest import mock
from toktokkie.Directory import Directory
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.types.MusicArtist import MusicArtist
from toktokkie.test.metadata.TestMetadata import _TestMetadata
from puffotter.os import listdir, makedirs


class TestMusicArtist(_TestMetadata):
    """
    Class that tests the MusicArtist metadata class
    """

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        amalee = self.get("AmaLee")
        amalee_dir = Directory(amalee)

        correct_files = []
        for album, album_path in listdir(amalee):
            for song, song_file in listdir(album_path):
                correct_files.append(song_file)

        amalee_dir.rename(noconfirm=True)

        for correct_file in correct_files:
            self.assertTrue(os.path.isfile(correct_file))

    def test_validation(self):
        """
        Tests if the validation of metadata works correctly
        :return: None
        """
        valid_data = [
            {
                "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            },
            {
                "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": ["bbb"]}
                }]
            }
        ]
        invalid_data = [
            {},
            {
                # book metadata type
                "type": "book", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            },
            {
                # Theme song name
                "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "B", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            },
            {
                # ID type
                "type": "music", "ids": {"tvdb": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            },
            {
                # Album ID type
                "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"tvdb": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            },
            {
                # ID is int
                "type": "music", "ids": {"musicbrainz_artist": [111]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            },
            {
                # Album ID is int
                "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": [111]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            },
            {
                "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": [111]}
                }]
            },
            {
                "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": "2019",
                    "ids": {"musicbrainz_release": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "op",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            },
            {
                "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
                "albums": [{
                    "name": "A", "genre": "B", "year": 2019,
                    "ids": {"musicbrainz_release": ["bbb"]}
                }],
                "theme_songs": [{
                    "name": "A", "theme_type": "AAA",
                    "series_ids": {"musicbrainz_recording": ["ccc"]}
                }]
            }
        ]
        amalee = self.get("AmaLee")
        self.check_validation(valid_data, invalid_data, MusicArtist, amalee)

    def test_checking(self):
        """
        Tests if the checking mechanisms work correctly
        :return: None
        """
        amalee = Directory(self.get("AmaLee"))
        self.assertTrue(amalee.check(False, False, {}))
        os.remove(os.path.join(amalee.meta_dir, "icons/main.png"))
        self.assertFalse(amalee.check(False, False, {}))
