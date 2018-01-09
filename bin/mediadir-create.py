#!/usr/bin/env python
"""
Copyright 2015-2017 Hermann Krumrey

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
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="The directory name")
    parser.add_argument("media_type", help="The media type")

    args = parser.parse_args()

    name = args.name
    media_type = args.media_type

    MetaDataManager.generate_media_directory(name, media_type)
