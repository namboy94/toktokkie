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

from toktokkie.enums import MediaType, IdType
from toktokkie.metadata.base.IdHelper import IdHelper
from toktokkie.test.TestFramework import _TestFramework


class TestIdHelper(_TestFramework):
    """
    Class that tests the IdHelper class
    """

    def test_generating_manga_url(self):
        """
        Tests generating a manga URL
        :return: None
        """
        anilist_url = IdHelper.generate_url_for_id(
            IdType.ANILIST, MediaType.BOOK, "123"
        )
        self.assertEqual(anilist_url, "https://anilist.co/manga/123")
