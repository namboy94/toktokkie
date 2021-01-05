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
from puffotter.os import touch, makedirs
from toktokkie.Directory import Directory
from toktokkie.exceptions import InvalidDirectoryState
from toktokkie.neometadata.enums import IdType
from toktokkie.neometadata.movie.Movie import Movie
from toktokkie.test.TestFramework import _TestFramework


class TestPromptingMovieMetadata(_TestFramework):
    """
    Class that tests the MoviePrompter class
    """

    def test_generating_new_movie(self):
        """
        Tests prompting for new book metadata
        :return: None
        """
        path = self.get("Edge of Tomorrow")
        makedirs(path)
        touch(os.path.join(path, "Edge of Tomorrow.mp4"))

        with patch("builtins.input", side_effect=[
            "",  # tags
            "", "tt1631867",  # IMDB ID
            "", "", "",  # Other IDs
        ]):
            metadata = Movie.from_prompt(path)
            metadata.write()

        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata.name, "Edge of Tomorrow")
        self.assertEqual(metadata.ids[IdType.IMDB], ["tt1631867"])

    def test_prompting_with_missing_book_file(self):
        """
        Tests if a missing book file is handled correctly while prompting
        :return: None
        """
        path = self.get("Edge of Tomorrow")
        os.makedirs(path)

        try:
            with patch("builtins.input", lambda x: print(x)):
                Movie.from_prompt(path)
            self.fail()
        except InvalidDirectoryState as e:
            self.assertEqual(str(e), "No movie file")

    def test_prompting_with_multiple_book_files(self):
        """
        Tests if a missing book file is handled correctly while prompting
        :return: None
        """
        path = self.get("Edge of Tomorrow")
        os.makedirs(path)
        touch(os.path.join(path, "Part 1.mp4"))
        touch(os.path.join(path, "Part 2.mp4"))

        try:
            with patch("builtins.input", lambda x: print(x)):
                Movie.from_prompt(path)
            self.fail()
        except InvalidDirectoryState as e:
            self.assertEqual(str(e), "More than one movie file")

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        matrix_two = self.get("The Matrix Reloaded (2003)")
        os.makedirs(matrix_two)
        touch(os.path.join(matrix_two, "x.mp4"))
        with patch("builtins.input", side_effect=[
            "scifi, unpopular", "tt0234215", "", "", ""
        ]):
            metadata = Movie.from_prompt(matrix_two)
            metadata.write()

        directory = Directory(matrix_two)

        self.assertTrue(os.path.isdir(directory.meta_dir))
        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata, directory.metadata)
        self.assertEqual(metadata.ids[IdType.IMDB], ["tt0234215"])
        self.assertEqual(metadata.ids[IdType.ANILIST], [])
        self.assertEqual(metadata.ids[IdType.MYANIMELIST], [])
        self.assertEqual(metadata.ids[IdType.KITSU], [])

        for invalid in [
            IdType.VNDB, IdType.MANGADEX, IdType.TVDB, IdType.ISBN
        ]:
            self.assertFalse(invalid in metadata.ids)

        for tag in ["scifi", "unpopular"]:
            self.assertTrue(tag in metadata.tags)
