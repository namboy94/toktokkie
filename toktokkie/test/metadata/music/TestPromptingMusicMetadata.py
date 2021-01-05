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
from unittest.mock import patch
from puffotter.os import makedirs
from toktokkie.Directory import Directory
from toktokkie.enums import IdType
from toktokkie.metadata.music.Music import Music
from toktokkie.test.TestFramework import _TestFramework


class TestPromptingMusicMetadata(_TestFramework):
    """
    Class that tests the MusicPrompter class
    """

    def test_prompting_music_metadata(self):
        """
        Tests prompting music metadata
        :return: None
        """
        path = self.get("fripSide")
        makedirs(os.path.join(path, "Only my Railgun"))
        makedirs(os.path.join(path, "infinite synthesis"))

        with patch("builtins.input", side_effect=[
            "",  # tags
            "",  # musicbrainz (auto-generated)
            #  Only my Railgun
            "Anime", "2009", "",  # Album
            "y", "OP",  # Theme song
            "114921", "", "", "6213", "", "",  # Ids
            # infinite synthesis
            "J-Pop", "2010", "", "n"
        ]):
            meta = Music.from_prompt(path)
            meta.write()

        self.assertEqual(meta.name, "fripSide")
        self.assertEqual(len(meta.albums), 2)
        self.assertEqual(len(meta.non_theme_song_albums), 1)
        self.assertEqual(len(meta.theme_songs), 1)
        only_my_railgun = meta.theme_songs[0]
        infinite_synthesis = meta.non_theme_song_albums[0]
        self.assertEqual(only_my_railgun.name, "Only my Railgun")
        self.assertEqual(infinite_synthesis.name, "infinite synthesis")

        self.assertEqual(only_my_railgun.series_ids[IdType.ANILIST], ["6213"])
        self.assertEqual(only_my_railgun.album.genre, "Anime")
        self.assertEqual(only_my_railgun.album.year, 2009)
        self.assertEqual(infinite_synthesis.genre, "J-Pop")
        self.assertEqual(infinite_synthesis.year, 2010)

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        yui = self.get("YUI")
        os.makedirs(yui)
        makedirs(os.path.join(yui, "HOLIDAYS IN THE SUN"))
        makedirs(os.path.join(yui, "again"))

        with patch("builtins.input", side_effect=[
            "anime, j-pop",
            "80d1d7e0-fdab-4009-8375-54bd63d74c0e",
            "J-Pop", "2010", "2508b36d-e788-486b-902f-8ad4cf09910f", "n",
            "Anime", "2009", "", "y",
            "OP", "85249", "", "44fac196-20fd-48d7-a545-b848d459059d",
            "5114", "", ""
        ]):
            metadata = Music.from_prompt(yui)
            metadata.write()

        directory = Directory(yui)
        directory.metadata.rename(noconfirm=True)

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
