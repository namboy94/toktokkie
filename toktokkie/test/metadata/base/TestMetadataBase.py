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
from unittest.mock import patch
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.metadata.enums import IdType
from toktokkie.test.TestFramework import _TestFramework


class TestMetadataBase(_TestFramework):
    """
    Class that tests core functionality of the MetadataBase class
    """

    def test_tags(self):
        """
        Tests setting and getting of metadata tags
        :return: None
        """
        tv = Tv(self.get("Over the Garden Wall"))
        self.assertEqual(tv.tags, [])
        tv.tags = ["One", "Two"]
        self.assertEqual(tv.tags, ["One", "Two"])
        self.assertEqual(tv.tags, tv.json["tags"])

    def test_generating_id_urls(self):
        """
        Tests generating urls for IDs
        :return: None
        """
        tv = Tv(self.get("Fullmetal Alchemist"))
        urls = tv.urls
        self.assertEqual(
            urls[IdType.ANILIST][0],
            "https://anilist.co/anime/121"
        )

    def test_string_representation(self):
        """
        Tests the string representation of the metadata
        :return: None
        """
        tv = Tv(self.get("Over the Garden Wall"))
        string = str(tv)
        self.assertTrue("Season 1" in string)
        self.assertTrue("tv" in string)
        self.assertTrue("imdb" in string)

    def test_equality(self):
        """
        Tests equality of metadata objects
        :return: None
        """
        one = Tv(self.get("Over the Garden Wall"))
        two = Tv(self.get("Over the Garden Wall"))
        self.assertFalse(one is two)
        self.assertEqual(one, two)
        self.assertNotEqual(one, 1)

    def test_directory_gen_on_write(self):
        """
        Tests generating the .meta directory if it does not exist while writing
        :return: None
        """
        tv = Tv(self.get("Over the Garden Wall"))
        self.assertTrue(os.path.isfile(tv.metadata_file))
        shutil.rmtree(os.path.join(tv.directory_path, ".meta"))
        self.assertFalse(os.path.isfile(tv.metadata_file))
        tv.write()
        self.assertTrue(os.path.isfile(tv.metadata_file))
        tv.write()
        self.assertTrue(os.path.isfile(tv.metadata_file))

    def test_deviantart_folder_icon_link_printing(self):
        """
        Tests the deviantart folder icon link printing
        :return: None
        """
        tv = Tv(self.get("Over the Garden Wall"))

        def check_link(string: str):

            if string.startswith("Search"):
                return

            self.assertEqual(
                string,
                "https://www.deviantart.com/popular-all-time/"
                "?section=&global=1&q=Over+the+Garden+Wall+folder+icon"
            )

        with patch("builtins.print", check_link):
            tv.print_folder_icon_source()

    def test_retrieving_icon_file_path(self):
        """
        Tests retrieving the icon file path of an icon
        :return: None
        """
        tv = Tv(self.get("Over the Garden Wall"))
        self.assertEqual(
            tv.get_icon_file("Season 1"),
            os.path.join(tv.icon_directory, "Season 1.png")
        )
        self.assertEqual(tv.get_icon_file("Season 2"), None)
