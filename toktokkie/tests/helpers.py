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


def create_temporary_tv_series_directories() -> str:
    
    temporary_directory = os.path.join(os.getcwd(), "temp_testing")
    
    test_show_one_directory = os.path.join(temporary_directory, "Test Show 1")
    test_show_two_directory = os.path.join(temporary_directory, "Test Show 2")
    test_show_three_directory = os.path.join(temporary_directory, "Test Show 3")
    test_show_four_directory = os.path.join(temporary_directory, "Test Show 4")
    test_show_five_directory = os.path.join(temporary_directory, "Test Show 5")
    
    os.makedirs(os.path.join(test_show_one_directory, ".meta"))
    os.makedirs(os.path.join(test_show_two_directory, ".meta"))
    os.makedirs(os.path.join(test_show_three_directory, ".meta"))
    os.makedirs(test_show_four_directory)
    os.makedirs(os.path.join(test_show_five_directory, ".meta"))

    touch(os.path.join(test_show_one_directory, ".meta", "type"), "tv_series")
    touch(os.path.join(test_show_two_directory, ".meta", "type"), "tv_series")
    touch(os.path.join(test_show_three_directory, ".meta", "type"), "other")

    return temporary_directory


def touch(path: str, initial_text: str = ""):
    with open(path, 'w') as touchfile:
        touchfile.write(initial_text)