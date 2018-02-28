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


class Resolution:
    """
    A resolution with an X and Y dimension
    """

    def __init__(self, string: str):
        """
        Initializes the resolution object based on a string in the
        format like 1920x1080. Errors in the string will raise a ValueError
        :param string: The string to parse
        """
        try:
            split = string.lower().split("x")
            self.x = int(split[0])
            self.y = int(split[1])
        except IndexError:
            raise ValueError()
