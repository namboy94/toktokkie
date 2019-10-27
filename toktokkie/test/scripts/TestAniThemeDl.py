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
import argparse
from unittest import mock
from toktokkie.test.TestFramework import _TestFramework
from toktokkie.scripts.AnimeThemeDlCommand import AnimeThemeDlCommand
from toktokkie.metadata.types.MusicArtist import MusicArtist
from toktokkie.metadata.ids.functions import minimize_ids
from toktokkie.metadata.ids.IdType import IdType


class TestAniThemeDl(_TestFramework):

    def test_downloading(self):

        path = self.get("anitheme")

        args = argparse.Namespace()
        args.__dict__["year"] = "2019"
        args.__dict__["season"] = "Fall"
        args.__dict__["out"] = path
        cmd = AnimeThemeDlCommand(args)

        with mock.patch("builtins.input", side_effect=["1", ""]):
            cmd.execute()

        momo = os.path.join(path, "ED/Momo Asakura")
        chico = os.path.join(path, "OP/CHiCO with HoneyWorks")
        self.assertTrue(os.path.isdir(momo))
        self.assertTrue(os.path.isdir(chico))
        self.assertEqual(len(os.listdir(momo)), 2)
        self.assertEqual(len(os.listdir(chico)), 2)

        momo_obj = MusicArtist(momo)
        chico_obj = MusicArtist(chico)
        self.assertEqual(momo_obj.name, "Momo Asakura")
        self.assertEqual(chico_obj.name, "CHiCO with HoneyWorks")

        self.assertEqual(
            minimize_ids(momo_obj.ids),
            {IdType.MUSICBRAINZ_ARTIST: ["0"]}
        )
        self.assertEqual(
            minimize_ids(chico_obj.ids),
            {IdType.MUSICBRAINZ_ARTIST: ["0"]}
        )

        shutil.rmtree(momo)
        shutil.rmtree(chico)

        self.assertFalse(os.path.isdir(momo))
        self.assertFalse(os.path.isdir(chico))

        with mock.patch("builtins.input", side_effect=["y", "y"]):
            cmd.execute()

        self.assertTrue(os.path.isdir(momo))
        self.assertTrue(os.path.isdir(chico))
