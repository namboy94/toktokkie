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

from toktokkie.verification import get_all_verificator_attributes
from toktokkie.test.verification.TestVerificator import TestVerificator
from toktokkie.verification.EntriesInAnilistVerificator import \
    EntriesInAnilistVerificator as SampleVerificator


class TestVerificatorAttributes(TestVerificator):
    """
    Class that tests the attributes of verificators
    """

    def test_attributes(self):
        """
        Tests the attributes of the verificators to check if they are
        valid. I.e. all contain at least a help and type argument.
        :return: None
        """
        for attribute, value in get_all_verificator_attributes().items():
            self.assertTrue("help" in value)
            self.assertTrue("type" in value)

            if "default" in value:
                self.assertTrue("choices" in value)

    def test_initializing_verificator_with_too_many_attributes(self):
        """
        Makes sure that superfluous attributes do not affect the verificator
        :return: None
        """
        _, _, anime_series, _, _ = self.generate_sample_metadata()
        verificator = SampleVerificator(anime_series, {
            "anilist_user": "namboy94",
            "extra": 123,
            "10000": 10000
        })
        self.assertEqual(verificator.username, "namboy94")

    def test_using_incorrect_type_as_attribute(self):
        """
        Checks if invalid types are correctly identified during initialization
        of the verificator
        :return: None
        """
        _, _, anime_series, _, _ = self.generate_sample_metadata()

        try:
            SampleVerificator(anime_series, {"anilist_user": 100})
            self.fail()
        except ValueError:
            pass
