"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

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
"""

from typing import List
from toktokkie.metadata.types.Language import Language
from toktokkie.metadata.types.Resolution import Resolution
from toktokkie.metadata.types.MetaType import MetaType, MetaPrimitive, Str, Int


class CommaList(MetaPrimitive):
    """
    A class that automatically splits up a string into a comma-separated list
    """

    def __init__(self, _list: List[MetaType]):
        """
        Initializes a comma list
        :param _list: The list to use
        """
        self.list = _list

    @classmethod
    def parse(cls, string: str):
        """
        Parses a comma-separated list
        :param string: The string to parse
        :return: The parsed list
        """
        parsed = string.split(",") if string != "" else []
        parsed = list(map(lambda x: Str(x), parsed))
        return cls(parsed)

    def __str__(self) -> str:
        """
        Provides a string representation of the comma-separated list
        :return: The string representation of the list
        """
        return str(self.list)

    def cast(self, cls: any) -> list:
        """
        Casts all elements in the list to the specified class
        :param cls: The class to which to cast to
        :return: The converted list of elements
        """
        return list(map(lambda x: cls(x), self.list))


class IntCommaList(CommaList):
    """
    A comma list specialized for integer values
    """

    def __init__(self, _list: List[MetaType]):
        """
        Casts the list values to int
        :param _list: The list to use
        """
        super().__init__(_list)
        self.list = self.cast(Int)


class ResolutionCommaList(CommaList):
    """
    A comma list specialized for Resolutions
    """

    def __init__(self, _list: List[MetaType]):
        """
        Casts the list to Resolution objects and turns them into
        dictionaries.
        :param _list: The list to use
        """
        super().__init__(_list)
        self.list = self.cast(Resolution)


class LanguageCommaList(CommaList):
    """
    A comma list specialized for language values
    """

    def __init__(self, _list: List[MetaType]):
        """
        Casts the list values to int
        :param _list: The list to use
        """
        super().__init__(_list)
        self.list = self.cast(Language)
