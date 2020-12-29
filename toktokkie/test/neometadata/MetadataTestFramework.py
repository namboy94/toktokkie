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
from unittest import TestCase


class _MetadataTestFramework(TestCase):
    """
    Framework for testing metadata classes
    """

    tmp_dir = "/tmp/toktokkie-test"
    """
    The path to the temporary test directory
    """

    res_dir = "/tmp/toktokkie-test/res"

    def setUp(self):
        self.cleanup()
        res_src = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "res"
        )
        shutil.copytree(res_src, self.res_dir)

    def tearDown(self):
        self.cleanup()

    def cleanup(self):
        if os.path.isdir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
