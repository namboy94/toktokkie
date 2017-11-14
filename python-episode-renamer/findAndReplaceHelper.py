"""
Copyright 2015-2017 Hermann Krumrey

This file is part of python-episode-renamer.

python-episode-renamer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python-episode-renamer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with python-episode-renamer.  If not, see <http://www.gnu.org/licenses/>.
"""

import os

find = raw_input("Enter the phrase to be replaced   ")
replace = raw_input("Enter the phrase to be substituted   ")
directory = raw_input("Enter the directory")
if not directory.endswith("/"):
    directory = directory + "/"

for fil in os.listdir(directory):
    fileName = directory + fil
    if find in fileName:
        replacementFileName = fileName.replace(find, replace)
        print "renaming"
        os.system("mv \"" + fileName + "\" \"" + replacementFileName + "\"")