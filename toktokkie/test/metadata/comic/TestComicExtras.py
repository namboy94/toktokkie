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
from toktokkie.metadata.comic.Comic import Comic
from toktokkie.test.TestFramework import _TestFramework


class TestComicExtras(_TestFramework):
    """
    Class that tests the ComicExtras class
    """

    def test_paths(self):
        """
        Tests the paths to the main and special directory
        :return: None
        """
        path = self.get("Taishou Otome Otogibanashi")
        meta = Comic(path)
        self.assertEqual(
            meta.main_path,
            os.path.join(path, "Main")
        )
        self.assertEqual(
            meta.special_path,
            os.path.join(path, "Special")
        )

    def test_special_chapters(self):
        """
        Tests retrieving the special chapters for the comic
        :return: None
        """
        path = self.get("Taishou Otome Otogibanashi")
        meta = Comic(path)
        specials = meta.special_chapters
        self.assertEqual(len(specials), 5)
        self.assertEqual(specials[0], "8.5")

        specials.append("123.5")
        meta.special_chapters = specials
        specials = meta.special_chapters
        self.assertEqual(len(specials), 6)
        self.assertEqual(specials[0], "8.5")

        specials.append("1.5")
        meta.special_chapters = specials
        specials = meta.special_chapters
        self.assertEqual(len(specials), 7)
        self.assertEqual(specials[0], "1.5")
