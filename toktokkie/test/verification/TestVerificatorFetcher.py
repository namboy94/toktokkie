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

from toktokkie.verification.FolderIconVerificator import FolderIconVerificator
from toktokkie.verification.SeasonMetadataVerificator import \
    SeasonMetadataVerificator
from toktokkie.verification import get_verificators, all_verificators
from toktokkie.test.verification.TestVerificator import TestVerificator


class TestVerificatorFetcher(TestVerificator):
    """
    Test class for the get_verificators method that makes it possible
    to get the correct verificators for any given metadata type
    """

    def test_fetching_verificators(self):

        base, tv_series, anime_series, movie, anime_movie = \
            self.generate_sample_metadata()

        for directory, expected in {
            base: [
                FolderIconVerificator
            ],
            tv_series: [
                FolderIconVerificator,
                SeasonMetadataVerificator
            ],
            anime_series: [
                FolderIconVerificator,
                SeasonMetadataVerificator
            ],
            movie: [
                FolderIconVerificator
            ],
            anime_movie: [
                FolderIconVerificator
            ]
        }.items():
            verificators = get_verificators(directory)
            verificator_types = list(map(lambda x: type(x), verificators))
            for verificator in expected:
                self.assertTrue(verificator in verificator_types)

            for verificator in all_verificators:
                if verificator not in expected:
                    self.assertFalse(verificator in verificator_types)
