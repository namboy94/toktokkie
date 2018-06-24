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
from toktokkie.Directory import Directory
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.SeasonMetadataVerificator import \
    SeasonMetadataVerificator


class TestSeasonMetadataVerificator(TestVerificator):

    media_dir = "test"
    """
    The directory in which to store the test media directory
    """

    verificator_cls = SeasonMetadataVerificator
    """
    The Verificator class to test
    """

    structure = {
        media_dir: {
            ".hidden": [],
            "file.txt": None,
            "Season 1": [],
            "Specials": []
        }
    }
    """
    The test directory structure
    """

    metadatas = {
        media_dir: TvSeries({
            "type": "tv_series",
            "name": "test",
            "tags": [],
            "seasons": [
                {
                    "path": "Season 1",
                    "name": "Season 1",
                    "tvdb_ids": [12345],
                    "audio_langs": ["eng"],
                    "subtitle_langs": ["eng"],
                    "resolutions": [{"x": 1920, "y": 1080}]
                },
                {
                    "path": "Specials",
                    "name": "Specials",
                    "tvdb_ids": [12345],
                    "audio_langs": ["eng"],
                    "subtitle_langs": ["eng"],
                    "resolutions": [{"x": 1920, "y": 1080}]
                }
            ],
            "tvdb_excludes": [],
            "tvdb_irregular_season_starts": [],
            "tvdb_multi_episodes": []
        })
    }
    """
    The metadata for the media directories
    """

    def test_with_missing_directories(self):
        """
        Tests if missing directories are accurately identified
        :return: None
        """
        verificator: SeasonMetadataVerificator = \
            self.verificators[self.media_dir]

        self.assertTrue(verificator.verify())

        for season in ["Season 1", "Specials"]:
            shutil.rmtree(os.path.join(verificator.directory.path, season))
            self.assertFalse(verificator.verify())
            self.setUp()

        os.remove(os.path.join(verificator.directory.path, "file.txt"))
        self.assertTrue(verificator.verify())

        shutil.rmtree(os.path.join(verificator.directory.path, ".hidden"))
        self.assertTrue(verificator.verify())

    def test_with_missing_entries(self):
        """
        Tests if missing entries in the metadata are correctly identified
        :return: None
        """

        verificator: SeasonMetadataVerificator = \
            self.verificators[self.media_dir]

        self.assertTrue(verificator.verify())
        self.assertEqual(2, len(verificator.directory.metadata.seasons.list))

        one = verificator.directory.metadata.seasons.pop(0)
        self.assertFalse(verificator.verify())

        two = verificator.directory.metadata.seasons.pop(0)
        self.assertFalse(verificator.verify())

        self.assertEqual(0, len(verificator.directory.metadata.seasons.list))

        verificator.directory.metadata.seasons.append(two)
        self.assertFalse(verificator.verify())

        verificator.directory.metadata.seasons.append(one)
        self.assertTrue(verificator.verify())

    def test_fixing_missing_directories(self):
        """
        Tests the fixing procedure of this verificator for missing directories
        :return: None
        """
        verificator: SeasonMetadataVerificator = \
            self.verificators[self.media_dir]

        season_one = os.path.join(verificator.directory.path, "Season 1")
        specials = os.path.join(verificator.directory.path, "Specials")

        shutil.rmtree(season_one)
        shutil.rmtree(specials)

        self.assertFalse(os.path.isdir(season_one))
        self.assertFalse(os.path.isdir(specials))

        verificator.fix()

        self.assertTrue(os.path.isdir(season_one))
        self.assertTrue(os.path.isdir(specials))
        self.assertTrue(verificator.verify())

    def test_fixing_missing_entries(self):
        """
        Tests fixing missing metadata entries via user prompts
        :return: None
        """

        verificator = self.verificators[
            self.media_dir
        ]  # type: SeasonMetadataVerificator

        one = verificator.directory.metadata.seasons.pop(0)
        two = verificator.directory.metadata.seasons.pop(0)

        self.assertFalse(verificator.verify())
        self.execute_with_mocked_input(
            ["", "12345", "eng", "eng", "1920x1080",
             "", "", "", "", ""],
            lambda: verificator.fix()
        )
        self.assertTrue(verificator.verify())

        written = Directory(verificator.directory.path)
        written_verificator = SeasonMetadataVerificator(written)
        self.assertTrue(written_verificator.verify())

        self.assertEqual(
            one.to_json(),
            written_verificator.directory.metadata.seasons.pop(0).to_json()
        )
        self.assertEqual(
            two.to_json(),
            written_verificator.directory.metadata.seasons.pop(0).to_json()
        )
