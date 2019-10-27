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

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        yui = self.get("YUI")
        os.makedirs(yui)
        makedirs(os.path.join(yui, "HOLIDAYS IN THE SUN"))
        makedirs(os.path.join(yui, "again"))

        with mock.patch("builtins.input", side_effect=[
            "anime, j-pop",
            "80d1d7e0-fdab-4009-8375-54bd63d74c0e",
            "J-Pop", "2010", "2508b36d-e788-486b-902f-8ad4cf09910f", "n",
            "Anime", "2009", "", "y",
            "OP", "85249", "", "44fac196-20fd-48d7-a545-b848d459059d",
            "5114", "", ""
        ]):
            metadata = MusicArtist.prompt(yui)
            metadata.write()

        directory = Directory(yui)
        directory.rename(noconfirm=True)

        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata, directory.metadata)

        self.assertEqual(metadata.tags, ["anime", "j-pop"])
        self.assertEqual(
            metadata.ids[IdType.MUSICBRAINZ_ARTIST],
            ["80d1d7e0-fdab-4009-8375-54bd63d74c0e"]
        )

        albums = metadata.albums
        holidays = albums[0]
        again = albums[1]
        again_theme = metadata.theme_songs[0]

        self.assertEqual(holidays.name, "HOLIDAYS IN THE SUN")
        self.assertEqual(holidays.year, 2010)
        self.assertEqual(holidays.genre, "J-Pop")
        self.assertEqual(
            holidays.ids[IdType.MUSICBRAINZ_RELEASE],
            ["2508b36d-e788-486b-902f-8ad4cf09910f"]
        )

        self.assertEqual(again.name, "again")
        self.assertEqual(again.year, 2009)
        self.assertEqual(again.genre, "Anime")
        self.assertEqual(again.ids[IdType.MUSICBRAINZ_RELEASE], [])

        self.assertEqual(again_theme.name, "again")
        self.assertEqual(again_theme.theme_type, "OP")
        self.assertEqual(
            again_theme.series_ids[IdType.MUSICBRAINZ_RECORDING],
            ["44fac196-20fd-48d7-a545-b848d459059d"]
        )
        self.assertEqual(again_theme.series_ids[IdType.TVDB], ["85249"])
        self.assertEqual(again_theme.series_ids[IdType.VNDB], [])
        self.assertEqual(again_theme.series_ids[IdType.MYANIMELIST], ["5114"])
        self.assertEqual(again_theme.series_ids[IdType.ANILIST], ["5114"])
        self.assertEqual(again_theme.series_ids[IdType.KITSU], [])

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
