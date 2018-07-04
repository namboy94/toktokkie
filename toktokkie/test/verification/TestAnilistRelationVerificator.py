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

from toktokkie.metadata.types.MetaType import Int
from toktokkie.verification.lib.anilist.enums import RelationType
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.lib.anilist.AnilistRelation import AnilistRelation
from toktokkie.verification.AnilistRelationVerificator \
    import AnilistRelationVerificator


class TestAnilistRelationVerificator(TestVerificator):
    """
    Class that tests if the AnilistRelationVerificator
    works correctly
    """

    prepared_directories = ["Steins;Gate", "91 Days"]
    """
    Prepared metadata directories.
    """

    verification_attr = {
        "anilist_user": "namboy94",
        "ignore_on_hold": True
    }
    """
    Verification attributes
    """

    verificator_cls = AnilistRelationVerificator
    """
    Verificator class to test
    """

    def setUp(self):
        """
        Creates easy to use instance variables for verificators
        :return: None
        """
        super().setUp()
        self.steinsgate, self.days = [
            self.verificators["Steins;Gate"],
            self.verificators["91 Days"]
        ]  # type: AnilistRelationVerificator

    def test_all_relations_satisfied(self):
        """
        Tests if the verificator correctly identifies all relations being
        satisfied
        :return: None
        """
        self.assertTrue(self.steinsgate.verify())

    def test_fictional_relation(self):
        """
        Tests how a non-real relation is handled
        :return: None
        """
        steinsgate_id = \
            self.steinsgate.directory.metadata.seasons.list[0].mal_ids.list[0]
        self.steinsgate.handler.entries[steinsgate_id].relations.append(
            AnilistRelation(steinsgate_id, 1, RelationType.SEQUEL)
        )
        self.assertFalse(self.steinsgate.verify())
        self.steinsgate.directory.metadata.mal_check_ignores.append(Int(1))
        self.steinsgate.directory.write_metadata()
        self.assertTrue(self.steinsgate.verify())
