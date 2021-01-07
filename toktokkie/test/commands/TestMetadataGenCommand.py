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
import shutil
from puffotter.os import makedirs, touch
from toktokkie.Directory import Directory
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.metadata.book.Book import Book
from toktokkie.enums import IdType, MediaType
from toktokkie.exceptions import MissingMetadata, InvalidMetadata
from toktokkie.test.TestFramework import _TestFramework


class TestMetadataGenCommand(_TestFramework):
    """
    Class that tests the metadata-gen command
    """

    def test_generating_metadata(self):
        """
        Tests using the command to create metadata
        :return: None
        """
        path = self.get("New")
        makedirs(path)

        try:
            Directory(path)
            self.fail()
        except MissingMetadata:
            pass

        # TV
        season = os.path.join(path, "Season 1")
        makedirs(season)
        self.execute_command(["metadata-gen", "tv", path], [
            "tag",
            "", "tt0903747", "", "", "",
            "", "", "", "", ""
        ])

        meta = Tv(path)
        self.assertEqual(meta.tags, ["tag"])
        self.assertEqual(meta.ids[IdType.IMDB], ["tt0903747"])
        self.assertEqual(meta.seasons[0].ids[IdType.IMDB], ["tt0903747"])

        try:
            Book(path)
            self.fail()
        except InvalidMetadata:
            pass

        self.assertEqual(
            Directory(path).metadata.media_type(),
            MediaType.TV_SERIES
        )

        # Book
        shutil.rmtree(season)
        touch(os.path.join(path, "book.txt"))
        self.execute_command(["metadata-gen", "book", path], [
            "y", "tag2", "ABC", "", "", ""
        ])

        meta = Book(path)
        self.assertEqual(meta.tags, ["tag2"])
        self.assertEqual(meta.ids[IdType.ISBN], ["ABC"])

        try:
            Tv(path)
            self.fail()
        except InvalidMetadata:
            pass

        self.assertEqual(
            Directory(path).metadata.media_type(),
            MediaType.BOOK
        )

    def test_generating_non_existant_directory(self):
        """
        Tests if attempting to generate metadata for a non-existing directory
        fails
        :return: None
        """
        # TODO maybe make a 'default' directory structure that is generated
        # TODO instead of failing
        path = self.get("Test")
        self.execute_command(["metadata-gen", "music", path], [])
        self.assertFalse(os.path.isdir(path))

    def test_generating_where_pre_prompt_fails(self):
        """
        Tests if attempting to generate metadata for a directory that
        does not successfully pass the pre-prompt checks fails
        :return: None
        """
        path = self.get("Test")
        makedirs(path)
        self.execute_command(["metadata-gen", "tv", path], [])
        self.assertEqual(os.listdir(path), [])
