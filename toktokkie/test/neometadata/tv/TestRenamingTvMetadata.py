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
from puffotter.os import listdir
from toktokkie.neometadata.enums import IdType
from toktokkie.Directory import Directory
from toktokkie.test.TestFramework import _TestFramework


class TestRenamingTvMetadata(_TestFramework):
    """
    Class that tests renaming the content of tv series metadata
    """

    def test_simple_renaming(self):
        otgw = self.get("Over the Garden Wall")
        otgw_dir = Directory(otgw)
        otgw_dir.rename(noconfirm=True)

        correct = []
        wrong = []
        for _, season_dir in listdir(otgw):
            for episode, episode_file in listdir(season_dir):
                new_file = os.path.join(season_dir, "A" + episode)
                os.rename(episode_file, new_file)
                correct.append(episode_file)
                wrong.append(new_file)

        for _file in correct:
            self.assertFalse(os.path.isfile(_file))
        for _file in wrong:
            self.assertTrue(os.path.isfile(_file))

        otgw_dir.rename(noconfirm=True)

        for _file in correct:
            print(_file)
            self.assertTrue(os.path.isfile(_file))
        for _file in wrong:
            self.assertFalse(os.path.isfile(_file))

        otgw_dir.metadata.set_ids(IdType.ANILIST, ["19815"])
        otgw_dir.rename(noconfirm=True)

        self.assertEqual(otgw_dir.metadata.name, "No Game, No Life")

        for _file in correct:
            self.assertFalse(os.path.isfile(_file))
