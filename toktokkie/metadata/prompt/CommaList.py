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

from typing import List, Any
from toktokkie.metadata.prompt.PromptType import PromptType


class CommaList(PromptType):
    """
    Class that allows the automatic conversion of user-provided strings to
    values
    """

    primitive = str
    """
    The primitive type to contain within the comma list
    """

    @property
    def value(self) -> List[Any]:
        """
        Converts the string value into its actual value
        :return: The generated value
        """
        values = []

        for split in self._value.split(","):
            values.append(self.primitive(split.strip()))

        return values


class IntCommaList(CommaList):
    """
    A comma list using integer values
    """

    primitive = int
    """
    The primitive type to contain within the comma list
    """
