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

import os
from typing import Dict


def get_metadata_paths() -> Dict[str, str]:
    """
    Retrieves a dictionary containing paths to metadata directories
    :return: The dictionary of metadata directory paths
    """

    this_dir = os.path.dirname(os.path.abspath(__file__))
    paths = {}
    for path in os.listdir(os.path.join(this_dir, "metadata")):
        paths[path] = os.path.join(this_dir, "metadata", path)
    return paths