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

import argparse


class ArgumentParser(object):
    """
    Class that handles parsing of arguments
    """

    def __init__(self):
        """
        Constructor
        Defines which options to be parsed
        :return: void
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-i", "--install", help="installs the program", action="store_true")
        self.parser.add_argument("-u", "--update", help="updates the program", action="store_true")

    def parse(self):
        """
        Starts the argument parser
        :return: void
        """
        return self.parser.parse_args()
