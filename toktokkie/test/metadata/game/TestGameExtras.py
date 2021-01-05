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
from puffotter.os import touch
from toktokkie.metadata.game.Game import Game
from toktokkie.test.TestFramework import _TestFramework


class TestGameExtras(_TestFramework):
    """
    Class that tests the GameExtras class
    """

    def test_bool_attributes(self):
        """
        Tests the class's boolean attributes
        :return: None
        """
        fureraba = Game(self.get("Fureraba"))
        self.assertEqual(fureraba.has_ed, True)
        self.assertEqual(fureraba.has_op, True)
        self.assertEqual(fureraba.has_cgs, True)
        self.assertEqual(fureraba.has_ost, False)

    def test_retrieving_extra_files(self):
        """
        Tests retrieving extra files like OST or CG files
        :return: None
        """
        fureraba = Game(self.get("Fureraba"))

        self.assertEqual(len(fureraba.ops), 1)
        self.assertEqual(len(fureraba.eds), 4)
        self.assertEqual(len(fureraba.ost), 0)
        self.assertEqual(len(fureraba.cgs), 3)
        print(fureraba.cgs["original"])
        self.assertEqual(len(fureraba.cgs["original"]), 609)

        shutil.rmtree(fureraba.video_dir)
        self.assertEqual(len(fureraba.ops), 0)
        self.assertEqual(len(fureraba.eds), 0)

        os.makedirs(os.path.join(fureraba.cg_dir, "new"))
        self.assertEqual(len(fureraba.cgs["new"]), 0)
        self.assertEqual(len(fureraba.cgs), 4)
        shutil.rmtree(fureraba.cg_dir)
        self.assertEqual(len(fureraba.cgs), 0)

        os.makedirs(fureraba.ost_dir)
        touch(os.path.join(fureraba.ost_dir, "test1.mp3"))
        touch(os.path.join(fureraba.ost_dir, "test2.mp3"))
        self.assertEqual(len(fureraba.ost), 2)
