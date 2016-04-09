"""
LICENSE:

Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.

LICENSE
"""

import math


class FileSizeCalculator(object):
    """
    class that offers methods to do calculations with file sizes
    """

    @staticmethod
    def get_byte_size_from_string(size_string):
        """
        Turns a size string into a byte integer
        """
        try:
            byte_size = int(size_string)
        except ValueError:
            byte_size = int(size_string[:-1])
            unit = size_string[-1:].lower()
            multiplier = 1
            if unit == "k":
                multiplier = math.pow(2, 10)
            elif unit in "m":
                multiplier = math.pow(2, 20)
            elif unit == "g":
                multiplier = math.pow(2, 30)
            elif unit == "b":
                new_unit = size_string[-2:]
                new_unit = new_unit[:-1]
                recursive_size_string = size_string[:-2] + new_unit
                return FileSizeCalculator.get_byte_size_from_string(recursive_size_string)
            byte_size *= multiplier
        return byte_size
