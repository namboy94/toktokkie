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
from jsonschema import validate, ValidationError
from toktokkie.neometadata.tv.Tv import Tv
from toktokkie.exceptions import InvalidMetadata
from toktokkie.test.TestFramework import _TestFramework


class TestValidatingTvMetadata(_TestFramework):
    """
    Class that tests validating tv series metadata
    """

    def test_json_validation(self):
        """
        Tests the JSON validation of the validator
        """

        valid_data = [
            {"type": "tv", "ids": {"tvdb": ["281643"]},
             "seasons": [{"name": "Season 1", "ids": {}}]}
        ]
        invalid_data = [
            # Missing required attrs
            {},
            # Missing seasons attribute
            {"type": "tv", "ids": {"tvdb": ["281643"]}},
            # missing ids attribute
            {"type": "tv", "seasons": [{"name": "Season 1", "ids": {}}]},
            # Wrong media type
            {"type": "movie", "ids": {"tvdb": ["281643"]},
             "seasons": [{"name": "Season 1", "ids": {}}]},
            # IDs not a list
            {"type": "tv", "ids": {"tvdb": [281643]},
             "seasons": [{"name": "Season 1", "ids": {}}]},
            # IDs are ints
            {"type": "tv", "ids": {"tvdb": [281643]},
             "seasons": [{"name": "Season 1", "ids": {}}]},
            # Invalid ID type
            {"type": "tv", "ids": {"isbn": ["281643"]},
             "seasons": [{"name": "Season 1", "ids": {}}]},
        ]
        schema = Tv.build_schema()

        for entry in valid_data:
            validate(entry, schema)
        for entry in invalid_data:
            try:
                validate(entry, schema)
                self.fail()
            except ValidationError:
                pass

    def test_structure_validation(self):
        """
        Tests the structural validation of the validator
        """

        valid_data = [
            {"type": "tv", "ids": {"tvdb": ["281643"]},
             "seasons": [{"name": "Season 1", "ids": {}}]}
        ]
        invalid_data = [
            # Additional season
            {"type": "tv", "ids": {"tvdb": ["281643"]},
             "seasons": [{"name": "Season 2", "ids": {}}]},
            # Missing season 1
            {"type": "tv", "ids": {"tvdb": ["281643"]},
             "seasons": []}
        ]
        schema = Tv.build_schema()
        otgw = self.get("Over the Garden Wall")

        for entry in valid_data:
            Tv(otgw, entry)
        for entry in invalid_data:
            validate(entry, schema)
            try:
                Tv(otgw, entry)
                self.fail()
            except InvalidMetadata:
                pass

    def test_missing_season_directory(self):
        """
        Tests if missing season directories are handled correctly
        """
        haruhi = Tv(self.get("The Melancholy of Haruhi Suzumiya"))
        haruhi.validate()

        new_dir = os.path.join(haruhi.directory_path, "New")
        os.makedirs(new_dir)

        try:
            haruhi.validate()
            self.fail()
        except InvalidMetadata:
            pass

    def test_missing_season_metadata(self):
        """
        Tests if missing season metadata is handled correctly
        """
        haruhi = Tv(self.get("The Melancholy of Haruhi Suzumiya"))
        haruhi.validate()

        s2 = os.path.join(haruhi.directory_path, "Season 2")
        shutil.rmtree(s2)

        try:
            haruhi.validate()
            self.fail()
        except InvalidMetadata:
            pass
