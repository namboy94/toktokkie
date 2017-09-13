"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

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
LICENSE
"""

import os
import shutil
import unittest
from toktokkie.utils.metadata.media_types.Base import Base
from toktokkie.utils.metadata.media_types.TvSeries import TvSeries
from toktokkie.utils.metadata.media_types.AnimeSeries import AnimeSeries
from toktokkie.utils.metadata.media_types.Ebook import Ebook
from toktokkie.utils.metadata.media_types.LightNovel import LightNovel


class MediaTypesUnitTests(unittest.TestCase):
    """
    Tests the Media Type classes
    """

    media_types = [Base, TvSeries, AnimeSeries, Ebook, LightNovel]

    def test_defining_attributes(self):
        """
        Tests defining the attributes of the various media types
        :return: None
        """
        for media_type in self.media_types:
            attrs = media_type.define_attributes()
            self.assertTrue("required" in attrs)
            self.assertTrue("optional" in attrs)
            self.assertTrue("extenders" in attrs)
            self.assertEqual(len(attrs), 3)

    def test_valid_json(self):
        """
        Tests if valid JSON files are read correctly
        :return: None
        """
        json_dir = "toktokkie/tests/resources/json/media_types/valid"
        for media_type in self.media_types:
            count = 0
            for json_file in os.listdir(json_dir):
                if json_file.startswith(media_type.identifier):
                    count += 1
                    if os.path.isdir("test_media_type"):
                        shutil.rmtree("test_media_type")
                    os.makedirs("test_media_type/.meta")
                    shutil.copyfile(os.path.join(json_dir, json_file), "test_media_type/.meta/info.json")
                    media_type("test_media_type")
                    shutil.rmtree("test_media_type")
            self.assertTrue(count > 0)

    def test_invalid_json(self):
        """
        Tests if incorrect JSON is detected correctly
        :return: None
        """
