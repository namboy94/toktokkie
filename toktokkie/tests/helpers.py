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
import shutil
from typing import List


test_dir = os.path.join(os.getcwd(), "temp_testing")


def create_temp_files_and_folders(folders: List[str], files: List[str]):
    for folder in folders:
        os.makedirs(os.path.join(test_dir, folder))
    for fil in files:
        touch(os.path.join(test_dir, fil))


def touch(path: str, initial_text: str = ""):
    with open(path, 'w') as touchfile:
        touchfile.write(initial_text)


def cleanup():
    shutil.rmtree(test_dir)
