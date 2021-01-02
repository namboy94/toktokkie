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
from unittest import mock
from toktokkie.Directory import Directory
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.types.BookSeries import BookSeries
from toktokkie.test.metadata.TestMetadata import _TestMetadata
from puffotter.os import listdir, create_file


class TestBookSeries(_TestMetadata):
    """
    Class that tests the BookSeries metadata class
    """



    def test_checking(self):
        """
        Tests if the checking mechanisms work correctly
        :return: None
        """
        bsb = Directory(self.get("Bluesteel Blasphemer"))
        self.assertTrue(bsb.check(False, False, {}))

        icon = os.path.join(bsb.meta_dir, "icons/main.png")
        os.remove(icon)
        self.assertFalse(bsb.check(False, False, {}))
        create_file(icon)
        self.assertTrue(bsb.check(False, False, {}))

        for volume, path in listdir(bsb.path, no_dirs=True):
            os.rename(path, os.path.join(bsb.path, "AAA" + volume))
        self.assertFalse(bsb.check(False, False, {}))
        bsb.rename(noconfirm=True)
        self.assertTrue(bsb.check(False, False, {}))
