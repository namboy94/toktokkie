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
from puffotter.os import makedirs, touch
from toktokkie.Directory import Directory
from toktokkie.metadata.enums import IdType
from toktokkie.metadata.comic.Comic import Comic
from toktokkie.test.TestFramework import _TestFramework


class TestPromptingComicMetadata(_TestFramework):
    """
    Class that tests the ComicPrompter class
    """

    def test_prompting_comic_series(self):
        """
        Tests prompting comic series
        :return: None
        """
        path = self.get("Tonikaku Kawaii")
        makedirs(path)
        with patch("builtins.input", side_effect=[
            "",  # tags
            "", "112589", "", "", "23439"  # IDs
        ]):
            metadata = Comic.from_prompt(path)
            metadata.write()
        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata.name, "Tonikaku Kawaii")
        self.assertEqual(metadata.ids[IdType.MYANIMELIST], ["112589"])
        self.assertEqual(metadata.ids[IdType.ANILIST], ["101177"])
        self.assertEqual(metadata.ids[IdType.MANGADEX], ["23439"])

    def test_prompting_comic_series_with_special_chapter(self):
        """
        Tests prompting comic series with special chapters
        :return: None
        """
        path = self.get("Tonikaku Kawaii")
        makedirs(path)
        makedirs(os.path.join(path, "Special"))
        with patch("builtins.input", side_effect=[
            "",  # tags
            "", "112589", "", "", "23439",  # IDs
            "0, 7.5, 20.5, 123.5, 123.6, 123.7, 250"  # Special chapters
        ]):
            metadata = Comic.from_prompt(path)
            metadata.write()
        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(
            metadata.special_chapters,
            ["0", "7.5", "20.5", "123.5", "123.6", "123.7", "250"]
        )

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        showa = self.get("Shouwa Otome Otogibanashi")
        os.makedirs(showa)
        os.makedirs(os.path.join(showa, "Special"))
        touch(os.path.join(showa, "Special/Chap 5.5.cbz"))
        with patch("builtins.input", side_effect=[
            "shouwa, romance, sequel", "", "", "106988", "", "", "5.5"
        ]):
            metadata = Comic.from_prompt(showa)
            metadata.write()

        directory = Directory(showa)

        self.assertTrue(os.path.isdir(directory.meta_dir))
        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata, directory.metadata)
        self.assertEqual(metadata.ids[IdType.ANILIST], ["106988"])
        self.assertEqual(metadata.ids[IdType.MYANIMELIST], [])
        self.assertEqual(metadata.ids[IdType.KITSU], [])
        self.assertEqual(metadata.ids[IdType.MANGADEX], [])
        self.assertEqual(metadata.ids[IdType.ISBN], [])
        self.assertEqual(metadata.special_chapters, ["5.5"])

        for invalid in [IdType.VNDB, IdType.IMDB, IdType.TVDB]:
            self.assertFalse(invalid in metadata.ids)

        for tag in ["shouwa", "romance", "sequel"]:
            self.assertTrue(tag in metadata.tags)

        special_file = os.path.join(
            showa, "Special/Shouwa Otome Otogibanashi - Chapter 5.5.cbz"
        )
        self.assertFalse(os.path.isfile(special_file))
        directory.rename(noconfirm=True)
        self.assertTrue(os.path.isfile(special_file))
