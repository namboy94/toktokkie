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
import time
from threading import Thread
from toktokkie.metadata.Base import Base
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.FolderIconVerificator import FolderIconVerificator


class TestFolderIconVerificator(TestVerificator):

    media_dir = "test"
    """
    The directory in which to store the test media directory
    """

    verificator_cls = FolderIconVerificator
    """
    The Verificator class to test
    """

    structure = {
        media_dir: {
            ".hidden": [],
            "Season 1": [],
            "Season 2": [],
            "Specials": [],
            ".meta": {
                "icons": [
                    "Season 1.png",
                    "Season 2.png",
                    "Specials.png",
                    "main.png",
                ]
            },
        }
    }
    """
    The test directory structure
    """

    metadatas = {
        media_dir: Base({
            "type": "base",
            "name": "test",
            "tags": []
        })
    }
    """
    The metadata for the media directories
    """

    def test_with_present_icon(self):
        """
        Tests if the verificator correctly finds the icon files
        :return: None
        """
        print(self.metadatas)
        self.assertTrue(self.verificators[self.media_dir].verify())

    def test_with_missing_icon(self):
        """
        Tests if missing icons are correctly identified
        :return: None
        """
        print(os.listdir(os.path.join(self.testdir, self.media_dir)))
        for icon in ["main", "Season 1", "Season 2", "Specials"]:
            iconfile = os.path.join(
                self.testdir, self.media_dir, ".meta/icons", icon + ".png"
            )
            os.remove(iconfile)
            self.assertFalse(self.verificators[self.media_dir].verify())
            self.setUp()

    def test_fixing(self):
        """
        Tests fixing the folder icon verificator's fixing functionality
        :return: None
        """

        missing_icon = os.path.join(
            self.testdir, self.media_dir, ".meta/icons/Season 1.png"
        )
        os.remove(missing_icon)

        def background():
            time.sleep(1)
            with open(missing_icon, "w") as f:
                f.write("TEST")

        user_input = [
            "y", "y", "y", "y", "y", "y",
            "n", "n", "n", "n", "n", "n",
            "y", "y", "y"
        ]
        n_called = {"status": False}

        def input_func(_: str):
            time.sleep(0.1)
            retval = user_input.pop(0)
            if retval == "n":
                n_called["status"] = True
            return retval

        verificator = \
            self.verificators[self.media_dir]  # type: FolderIconVerificator
        verificator.input_function = input_func

        self.assertFalse(verificator.verify())
        self.assertFalse(os.path.isfile(missing_icon))

        Thread(target=background).start()
        verificator.fix()

        self.assertTrue(os.path.isfile(missing_icon))
        self.assertTrue(verificator.verify())
        self.assertTrue(n_called["status"])
