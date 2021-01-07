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
from unittest.mock import patch
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.test.TestFramework import _TestFramework


class TestMetadataValidateCommand(_TestFramework):
    """
    Class that tests the metadata-validate command
    """

    def test_validation(self):
        """
        Tests the validation of directories
        :return: None
        """
        class DummyLogger:

            # noinspection PyPep8Naming
            @staticmethod
            def getLogger(_):
                return DummyLogger()

            def warning(self, _):
                raise ZeroDivisionError()

            def debug(self, _):
                pass

        with patch("toktokkie.Directory.logging", DummyLogger):

            self.execute_command([
                "metadata-validate",
                self.get("Faust"),
                self.get("Bluesteel Blasphemer"),
                self.get("The Matrix (1999)"),
                self.get("Over the Garden Wall")
            ], [])

            try:
                self.execute_command(["metadata-validate", "AAA"], [])
                self.fail()
            except ZeroDivisionError:
                pass

            path = self.get("Over the Garden Wall")
            meta = Tv(path)
            meta.json.pop("seasons")
            meta.write()

            try:
                self.execute_command(["metadata-validate", path], [])
                self.fail()
            except ZeroDivisionError:
                pass
