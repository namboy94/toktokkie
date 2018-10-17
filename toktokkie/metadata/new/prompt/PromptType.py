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


class PromptType:
    """
    Class that allows the automatic conversion of user-provided strings to
    values
    """

    def __init__(self, value: str):
        """
        Initializes the prompt type
        :param value: The string value to parse
        """
        self._value = value
        # noinspection PyStatementEffect
        self.value

    @property
    def value(self):
        """
        Converts the string value into its actual value
        :return: The generated value
        """
        raise NotImplementedError()
