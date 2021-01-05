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

from toktokkie.exceptions import InvalidMetadata
from toktokkie.metadata.music.Music import Music
from toktokkie.test.TestFramework import _TestFramework


class TestValidatingMusicMetadata(_TestFramework):
    """
    Class that tests the MusicVaildator class
    """

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
        self.perform_json_validation(Music, valid_data, invalid_data)

    def test_mismatching_album_names(self):
        """
        Tests if name mismatches between theme songs and albums are detected
        :return: None
        """
        data = {
            "type": "music", "ids": {"musicbrainz_artist": ["aaa"]},
            "albums": [{
                "name": "A", "genre": "B", "year": 2019,
                "ids": {"musicbrainz_release": ["bbb"]}
            }],
            "theme_songs": [{
                "name": "B", "theme_type": "op",
                "series_ids": {"musicbrainz_recording": ["ccc"]}
            }]
        }
        try:
            Music(self.get("AmaLee"), data)
            self.fail()
        except InvalidMetadata:
            pass
