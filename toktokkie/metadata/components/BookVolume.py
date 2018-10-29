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
from toktokkie.exceptions import InvalidMetadataException
from toktokkie.metadata.components.MetadataPart import MetadataPart


class BookVolume(MetadataPart):
    """
    Class that models a single book volume
    """

    def validate(self):
        """
        Validates the JSON data of the book volume.
        :return: None
        :raises InvalidMetadataException: If something is wrong
                                          with the JSON data
        """
        super().validate()
        if not os.path.isfile(self.path):
            raise InvalidMetadataException()
