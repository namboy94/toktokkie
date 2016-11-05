#!/usr/bin/env python
# coding=utf-8

"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

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
LICENSE
"""

# imports
import os
import sys
from toktokkie.utils.xdcc.updating.JsonHandler import JsonHandler


if __name__ == "__main__":

    # noinspection PyShadowingBuiltins
    json_file = "series.json" if len(sys.argv) == 2 else json_file = sys.argv[1]

    if not os.path.isfile(json_file):
        print(json_file + " does not exist.")
        sys.exit(1)

    handler = JsonHandler(json_file)

    for series in handler.get_series():
        series.update()
