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

import json
from toktokkie.metadata.Base import Base
from toktokkie.metadata.TvSeries import TvSeries

metadata_types = [Base, TvSeries]
"""
All available metadata types
"""


def resolve_metadata(metadata_file: str) -> Base:
    """
    Automatically resolves a metadata type based on the info.json's metadata
    type parameter.
    :param metadata_file: The metadata file for which to resolve the metadata
    :return: The read metadata file
    """
    with open(metadata_file, "r") as f:
        data = json.load(f)

    metadata_class = \
        list(filter(lambda x: x.type == data["type"], metadata_types))[0]

    return metadata_class.from_json_file(metadata_file)
