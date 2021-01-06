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
from typing import List, Tuple
from unittest.mock import patch
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.utils.iconizing.procedures.Procedure import Procedure
from toktokkie.utils.iconizing.Iconizer import Iconizer
from toktokkie.test.TestFramework import _TestFramework
from toktokkie.utils.iconizing.procedures.NoopProcedure import NoopProcedure
from toktokkie.utils.iconizing.procedures.GnomeProcedure import GnomeProcedure


class DummyProcedure(Procedure):
    """
    Class that keeps track of the iconizing efforts of an iconizing procedure
    """

    history: List[Tuple[str, str]] = []
    """
    History of the procedure
    """

    @classmethod
    def iconize(cls, directory: str, png_icon_path: str):
        """
        Keeps track of iconizing history
        :param directory: The directory to iconize
        :param png_icon_path: The PNG file
        :return: None
        """
        cls.history.append((directory, png_icon_path))

    @classmethod
    def is_applicable(cls) -> bool:
        """
        :return: True
        """
        return True


class TestIconizer(_TestFramework):
    """
    Tests for the Iconizer class
    """

    def cleanup(self):
        """
        Resets the DummyProcedure
        :return: None
        """
        super().cleanup()
        DummyProcedure.history = []

    def test_iconizing(self):
        """
        Tests simple iconizing
        :return: None
        """
        path = self.get("Over the Garden Wall")
        metadata = Tv(path)
        os.makedirs(os.path.join(path, "Season 2"))
        iconizer = Iconizer(metadata, DummyProcedure())
        iconizer.iconize()

        self.assertEqual(
            DummyProcedure.history,
            [
                (path, metadata.get_icon_file("main")),
                (os.path.join(path, "Season 1"),
                 metadata.get_icon_file("Season 1")),
                (os.path.join(path, "Season 2"),
                 metadata.get_icon_file("main"))
            ]
        )

    def test_getting_default_procedure(self):
        """
        Tests getting the default procedure
        :return: None
        """
        with patch("toktokkie.utils.iconizing.procedures.GnomeProcedure."
                   "GnomeProcedure.is_applicable", side_effect=[False]):
            default = Iconizer.default_procedure()
            self.assertEqual(default, NoopProcedure)
        with patch("toktokkie.utils.iconizing.procedures.GnomeProcedure."
                   "GnomeProcedure.is_applicable", side_effect=[True]):
            default = Iconizer.default_procedure()
            self.assertEqual(default, GnomeProcedure)

    def test_noop_procedure(self):
        """
        Tests the NoopProcedure
        :return: None
        """
        self.assertTrue(NoopProcedure.is_applicable())
        NoopProcedure.iconize("", "")
