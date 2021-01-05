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
from toktokkie.metadata.enums import IdType
from toktokkie.metadata.movie.Movie import Movie
from toktokkie.test.TestFramework import _TestFramework


class TestRenamingMovieMetadata(_TestFramework):
    """
    Class that tests the MovieRenamer class
    """

    def test_renaming_movie(self):
        """
        Tests renaming a movie
        :return: None
        """
        matrix = Movie(self.get("The Matrix (1999)"))
        og_file = matrix.movie_path
        og_dir = matrix.directory_path
        os.rename(og_file, os.path.join(matrix.directory_path, "a.mp4"))
        matrix.name = "The Matrix"

        self.assertFalse(os.path.isfile(og_file))
        self.assertFalse(os.path.isdir(og_dir))

        matrix.rename(noconfirm=True)

        self.assertTrue(os.path.isfile(og_file))
        self.assertTrue(os.path.isdir(og_dir))

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        path = self.get("The Matrix (1999)")
        meta = Movie(path)
        correct = os.path.join(path, "The Matrix (1999).mp4")
        incorrect = os.path.join(path, "The Matrix (2000).mp4")
        os.rename(correct, incorrect)

        self.assertFalse(os.path.isfile(correct))
        self.assertTrue(os.path.isfile(incorrect))

        meta.rename(noconfirm=True)

        self.assertTrue(os.path.isfile(correct))
        self.assertFalse(os.path.isfile(incorrect))

        meta.set_ids(IdType.IMDB, ["0"])
        meta.set_ids(IdType.ANILIST, ["431"])
        meta.rename(noconfirm=True)

        self.assertEqual(meta.name, "Howl‘s Moving Castle (2004)")
        self.assertFalse(os.path.isfile(correct))
        self.assertTrue(os.path.isfile(
            self.get("Howl‘s Moving Castle (2004)/"
                     "Howl‘s Moving Castle (2004).mp4")
        ))

    def test_renaming_title_if_invalid(self):
        """
        Tests how the renaming of the title is handled if no valid
        data can be fetched
        :return: None
        """
        matrix = Movie(self.get("The Matrix (1999)"))
        matrix.ids = {IdType.IMDB: ["0"]}
        matrix.name = "ABC"
        matrix.rename(noconfirm=True)
        self.assertEqual("ABC", matrix.name)
