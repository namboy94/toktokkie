"""
Copyright 2015-2017 Hermann Krumrey

This file is part of tvdb-episode-renamer.

tvdb-episode-renamer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tvdb-episode-renamer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with tvdb-episode-renamer.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Main script
@author Hermann Krumrey
"""
import argparse
from renamer.CLI import CLI
from renamer.GUI import GUI

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cli", help="Starts the program in CLI mode", action="store_true")
parser.add_argument("-d", "--directory", help="Starts the program and renames using a single directory")
args = parser.parse_args()

if args.cli:
    cli = CLI(args.directory)
    cli.start()
else:
    gui = GUI()