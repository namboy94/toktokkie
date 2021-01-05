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
from toktokkie.Directory import Directory
from toktokkie.enums import IdType
from toktokkie.metadata.game.Game import Game
from toktokkie.test.TestFramework import _TestFramework


class TestPromptingGameMetadata(_TestFramework):
    """
    Class that tests the GamePrompter class
    """

    def test_prompt(self):
        """
        Tests generating a new metadata object using user prompts
        :return: None
        """
        evangile = self.get("Princess Evangile")
        os.makedirs(evangile)

        with patch("builtins.input", side_effect=[
            "moege, school", "v6710"
        ]):
            metadata = Game.from_prompt(evangile)
            metadata.write()

        directory = Directory(evangile)

        self.assertTrue(os.path.isdir(directory.meta_dir))
        self.assertTrue(os.path.isfile(metadata.metadata_file))
        self.assertEqual(metadata, directory.metadata)
        self.assertEqual(metadata.ids[IdType.VNDB], ["v6710"])

        for id_type in IdType:
            if id_type not in [IdType.VNDB]:
                self.assertFalse(id_type in metadata.ids)

        for tag in ["school", "moege"]:
            self.assertTrue(tag in metadata.tags)
