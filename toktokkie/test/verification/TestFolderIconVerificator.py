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
from toktokkie.Directory import Directory
from toktokkie.metadata.Base import Base
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.FolderIconVerificator import FolderIconVerificator


class TestFolderIconVerificator(TestVerificator):

    media_dir = "test"
    seasons = ["Season 1", "Season 2", "Specials"]
    verificator = None

    def setUp(self):
        super().setUp()
        self.generate_structure({
            self.media_dir: {
                self.seasons[0]: [],
                self.seasons[1]: [],
                self.seasons[2]: [],
                ".meta": {
                    "icons": [
                        self.seasons[0] + ".png",
                        self.seasons[1] + ".png",
                        self.seasons[2] + ".png",
                        "main.png",
                    ]
                }
            }
        })
        Base({
            "type": "base",
            "name": "test",
            "tags": []
        }).write(os.path.join(self.testdir, "test/.meta/info.json"))
        directory = Directory(os.path.join(self.testdir, self.media_dir))
        self.verificator = FolderIconVerificator(directory)

    def test_with_present_icon(self):
        """
        Tests if the verificator correctly finds the icon files
        :return: None
        """
        self.assertTrue(self.verificator.verify())

    def test_with_missing_icon(self):
        for icon in self.seasons + ["main"]:
            iconfile = os.path.join(
                self.testdir, self.media_dir, ".meta/icons", icon + ".png"
            )
            os.remove(iconfile)
            self.assertFalse(self.verificator.verify())
            self.setUp()
