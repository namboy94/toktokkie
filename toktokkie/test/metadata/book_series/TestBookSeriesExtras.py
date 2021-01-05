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
from puffotter.os import touch
from toktokkie.enums import IdType
from toktokkie.metadata.book_series.components.BookVolume import BookVolume
from toktokkie.metadata.book_series.BookSeries import BookSeries
from toktokkie.test.TestFramework import _TestFramework


class TestBookSeriesExtras(_TestFramework):
    """
    Class that tests the BookSeriesExtras class
    """

    def test_volumes_attribute(self):
        """
        Tests the volumes getter and setter attributes
        :return: None
        """
        path = self.get("Bluesteel Blasphemer")
        meta = BookSeries(path)
        volumes = meta.volumes
        self.assertEqual(max(volumes.keys()), 4)

        vol_3 = volumes[3]
        self.assertEqual(vol_3.number, 3)
        self.assertEqual(vol_3.ids, meta.ids)
        self.assertEqual(
            os.path.join(path, "Bluesteel Blasphemer - Volume 3.epub"),
            vol_3.path
        )

        new_path = os.path.join(path, "Z.epub")
        touch(new_path)
        new_vol = BookVolume.from_json(
            5,
            new_path,
            meta.ids,
            {"ids": {IdType.ISBN.value: ["ABC"]}}
        )
        volumes[5] = new_vol
        meta.volumes = volumes

        meta.rename(noconfirm=True)
        self.assertTrue(os.path.exists(
            os.path.join(path, "Bluesteel Blasphemer - Volume 5.epub")
        ))
        self.assertEqual(len(meta.volumes), 5)
