"""
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
"""


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
                multiplier = 1000
            elif unit == "m":
                multiplier = 1000000
            elif unit == "g":
                multiplier = 1000000000
            byte_size *= multiplier
        return byte_size
