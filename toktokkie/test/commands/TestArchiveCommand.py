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
from toktokkie.test.TestFramework import _TestFramework


class TestArchiveCommand(_TestFramework):
    """
    Class that tests the archive command
    """

    aimer_archive = "Aimer.archive"

    def cleanup(self):
        """
        Performs cleanup operations
        :return: None
        """
        super().cleanup()
        if os.path.isdir(self.aimer_archive):
            shutil.rmtree(self.aimer_archive)

    def test_archiving(self):
        """
        Tests archiving metadata directories
        :return: None
        """
        path = self.get("Aimer")
        default_backup = self.aimer_archive
        specific_backup = self.get("Aimerback")
        multi_backup = self.get("Multi")

        self.execute_command(["archive", path], [])
        self.assertTrue(os.path.isdir(default_backup))
        metadir = os.path.join(default_backup, ".meta")
        self.assertTrue(os.path.isdir(metadir))
        shutil.rmtree(metadir)
        self.execute_command(["archive", path], ["n"])
        self.assertFalse(os.path.isdir(metadir))
        self.execute_command(["archive", path], ["y"])
        self.assertTrue(os.path.isdir(metadir))

        self.execute_command(["archive", path, "-o", specific_backup], [])
        self.assertTrue(os.path.isdir(specific_backup))
        self.assertTrue(os.path.isdir(os.path.join(specific_backup, ".meta")))

        self.execute_command(
            ["archive", path, self.get("Faust"), "-o", multi_backup], []
        )
        self.assertTrue(os.path.isdir(multi_backup))
        self.assertTrue(os.path.isdir(os.path.join(multi_backup, "Aimer")))
        self.assertTrue(
            os.path.isdir(os.path.join(multi_backup, "Aimer/.meta"))
        )
