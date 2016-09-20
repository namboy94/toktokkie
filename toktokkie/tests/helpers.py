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


def create_filled_temp_folder():

    try:
        cleanup()
    except FileNotFoundError:
        pass

    generic_episodes = {}
    for x in range(1, 16):
        generic_episodes["Episode " + str(x) + ".mkv"] = ""

    metatype_tv_series = {"type": "tv_series"}

    # directory is:
    # {directory: [(subdirectory_name, {file: content})]

    directories = {"Game of Thrones": {".meta": metatype_tv_series,
                                       "Season 1": generic_episodes,
                                       "Season 2": generic_episodes,
                                       "Specials": generic_episodes},
                   "Re Zero": {".meta": metatype_tv_series,
                               "Season 1": generic_episodes,
                               "OVA": generic_episodes,
                               "Specials": generic_episodes},
                   "The Big Bang Theory": {".meta": metatype_tv_series,
                                           "Season 1": generic_episodes,
                                           "Season 2": generic_episodes,
                                           "Season 3": generic_episodes,
                                           "Season 4": generic_episodes,
                                           "Season 5": generic_episodes},
                   "Random Folder": {}}

    for directory in directories:
        directory_path = os.path.join(test_dir, directory)
        os.makedirs(directory_path)
        for subdirectory in directories[directory]:
            subdirectory_path = os.path.join(directory_path, subdirectory)
            os.makedirs(subdirectory_path)
            for temp_file in directories[directory][subdirectory]:
                file_path = os.path.join(subdirectory_path, temp_file)
                content = directories[directory][subdirectory][temp_file]
                # noinspection PyTypeChecker
                touch(file_path, content)


def touch(path: str, initial_text: str = ""):
    with open(path, 'w') as touchfile:
        touchfile.write(initial_text)


def cleanup():
    shutil.rmtree(test_dir)
