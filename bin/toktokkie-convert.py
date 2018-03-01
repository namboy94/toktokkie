#!/usr/bin/env python

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

import argparse
from toktokkie import Directory


def main():
    """
    The toktokkie-iconize main method
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("directories", nargs="+")
    args = parser.parse_args()

    for path in args.directories:
        directory = Directory(path)
        print(directory.metadata.to_json())
        directory.metadata.write(directory.metadata_file)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Thanks for using toktokkie!")
