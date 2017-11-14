"""
Copyright 2015-2017 Hermann Krumrey

This file is part of nautilus-folder-iconizer.

nautilus-folder-iconizer is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nautilus-folder-iconizer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with nautilus-folder-iconizer.
If not, see <http://www.gnu.org/licenses/>.
"""

'''
main
The main program that ties the whole project together

Created on Apr 25, 2015
Modified on May 19, 2015

@author Hermann Krumrey
@version 1.3
'''

#imports
import sys
import os
from program.utils.ParserCollection import directoryChangeParser,getActiveDirectory,iconParser

#fix pythonpath
splitPath = sys.argv[0].split("/")
lengthToCut = len(splitPath[len(splitPath) - 1]) + len(splitPath[len(splitPath) - 2]) + 2
upperDirectory = sys.argv[0][:-lengthToCut]
sys.path.append(upperDirectory)

#check for root
#if os.geteuid() != 0:
#    sys.exit("This nautilus-foldericons needs root priviliges.")

configFileLocation = upperDirectory + "/nautilus-foldericons/data/config.txt"
warningFileLocation = upperDirectory + "/nautilus-foldericons/data/warnings.txt"
defaultIcons = upperDirectory + "/nautilus-foldericons/resources/"
directoryChangeParser(configFileLocation)
activeDirectory = getActiveDirectory(configFileLocation)

iconParser(activeDirectory, warningFileLocation, defaultIcons)