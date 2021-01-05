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
from puffotter.os import touch
from unittest.mock import patch
from toktokkie.Directory import Directory
from toktokkie.exceptions import InvalidDirectoryState
from toktokkie.metadata.enums import IdType
from toktokkie.metadata.book_series.BookSeries import BookSeries
from toktokkie.test.TestFramework import _TestFramework


class TestPromptingBookSeriesMetadata(_TestFramework):
    """
    Class that tests the BookSeriesPrompter class
    """

    def test_prompting_new_book_series(self):
        """
        Tests prompting a new book series
        :return: None
        """
        path = self.get("Arifureta")
        os.makedirs(path)
        touch(os.path.join(path, "Volume 1.epub"))
        touch(os.path.join(path, "Volume 2.epub"))
        with patch("builtins.input", side_effect=[
            "",  # tags
            "1", "", "86274", "",  # IDs
            "2", "", "", "",  # Volume 1 IDs
            "3", "", "100", ""  # Volume 2 IDs
        ]):
            meta = BookSeries.from_prompt(path)

        self.assertEqual(meta.ids[IdType.ISBN], ["1"])
        self.assertEqual(meta.ids[IdType.ANILIST], ["86274"])

        volumes = meta.volumes
        self.assertEqual(len(volumes), 2)
        self.assertEqual(volumes[1].ids[IdType.ISBN], ["2"])
        self.assertEqual(volumes[1].ids[IdType.ANILIST], ["86274"])
        self.assertEqual(volumes[2].ids[IdType.ISBN], ["3"])
        self.assertEqual(volumes[2].ids[IdType.ANILIST], ["100"])

    def test_prompting_without_book_files(self):
        """
        Tests if missing book files are detected prior to prompting
        :return: None
        """
        path = self.get("Arifureta")
        os.makedirs(path)
        try:
            with patch("builtins.input", lambda x: print(x)):
                BookSeries.prompt(path)
            self.fail()
        except InvalidDirectoryState:
            pass

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        sp_n_wo = self.get("Spice & Wolf")
        os.makedirs(sp_n_wo)
        touch(os.path.join(sp_n_wo, "Volume 1.epub"))
        touch(os.path.join(sp_n_wo, "Volume 2.epub"))

        with patch("builtins.input", side_effect=[
            "anime, holo",
            "", "9115", "", "",
            "ABC", "", "", "",
            "", "", "100685", "1"
        ]):
            metadata = BookSeries.from_prompt(sp_n_wo)
            metadata.write()

        directory = Directory(sp_n_wo)
        directory.rename(noconfirm=True)

        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata, directory.metadata)
        self.assertEqual(metadata.ids[IdType.ISBN], [])
        self.assertEqual(metadata.ids[IdType.ANILIST], ["39115"])
        self.assertEqual(metadata.ids[IdType.MYANIMELIST], ["9115"])
        self.assertEqual(metadata.ids[IdType.KITSU], [])
        self.assertEqual(metadata.volumes[1].ids[IdType.ISBN], ["ABC"])
        self.assertEqual(metadata.volumes[1].ids[IdType.ANILIST], ["39115"])
        self.assertEqual(metadata.volumes[1].ids[IdType.MYANIMELIST], ["9115"])
        self.assertEqual(metadata.volumes[1].ids[IdType.KITSU], [])
        self.assertEqual(metadata.volumes[2].ids[IdType.ISBN], [])
        self.assertEqual(metadata.volumes[2].ids[IdType.ANILIST], ["100685"])
        self.assertEqual(metadata.volumes[2].ids[IdType.MYANIMELIST], ["9115"])
        self.assertEqual(metadata.volumes[2].ids[IdType.KITSU], ["1"])

        for invalid in [IdType.VNDB, IdType.MANGADEX, IdType.TVDB]:
            self.assertFalse(invalid in metadata.ids)
            for _, volume in metadata.volumes.items():
                self.assertFalse(invalid in volume.ids)

        for tag in ["anime", "holo"]:
            self.assertTrue(tag in metadata.tags)
