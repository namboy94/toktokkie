#!/usr/bin/python
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
from toktokkie.scripts.manga_updater import start

# Add as many manga series as you want
# Don't forget to separate the dictionaries (parts enclosed in curly brackets {}) with commas
config = [

    {"target_directory": "Target Directory 1",
     "manga_url": "http://mangasite.domain/path/to/manga1"},

    {"target_directory": "Target Directory 2",
     "manga_url": "http://mangasite.domain/path/to/manga2"}

]

if __name__ == '__main__':

    # Uncomment options that you would like to use
    start(config,
          max_threads=50,
          # repair=True,
          # verbose=True,
          # dry_run=True
          )
