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


class MetaType:
    """
    All metadata parameters must implement a to_json method
    """

    def to_json(self) -> any:
        """
        Converts the object into a JSON-compatible object.
        By default, the object itself will be returned
        :return: A JSON-compatible representation of the object
        """
        return self


# noinspection PyAbstractClass
class MetaPrimitive(MetaType):
    """
    A class that, in addition to a to_json method, requires the implementation
    of a parse() method that parses a string and generates a corresponding
    object
    """

    @classmethod
    def parse(cls, string: str):
        """
        Parses a string to generate an object
        By default, the string is simply used as the only parameter of
        the constructor.
        :param string: The string
        :return: The generates object
        """
        # noinspection PyArgumentList
        return cls(string)


class Str(str, MetaPrimitive):
    """
    A class that implements a String primitive
    """
    pass


class Int(int, MetaPrimitive):
    """
    A class that implements an Integer primitive
    """
    pass
