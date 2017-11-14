"""
Copyright 2015-2017 Hermann Krumrey

This file is part of unix-episode-renamer.

unix-episode-renamer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

unix-episode-renamer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with unix-episode-renamer.  If not, see <http://www.gnu.org/licenses/>.
"""

'''
main
The main program that ties the whole project together

Created on Apr 25, 2015
Modified on May 2, 2015

@author Hermann Krumrey
@version 1.0
'''

#imports
import sys
import platform
from program.utils.userInputParser import parseUserInput
from program.utils.InputGUI import InputGUI

if platform.system() == "Linux":
    #fix pythonpath
    splitPath = sys.argv[0].split("/")
    lengthToCut = len(splitPath[len(splitPath) - 1]) + len(splitPath[len(splitPath) - 2]) + 2
    upperDirectory = sys.argv[0][:-lengthToCut]
    sys.path.append(upperDirectory)
    
    configFile = upperDirectory + "/program/data/config.txt"

elif platform.system() == "Windows":
    #fix pythonpath
    splitPath = sys.argv[0].split("\\")
    lengthToCut = len(splitPath[len(splitPath) - 1]) + len(splitPath[len(splitPath) - 2]) + 2
    upperDirectory = sys.argv[0][:-lengthToCut]
    sys.path.append(upperDirectory)
    
    configFile = upperDirectory + "\\program\\data\\config.txt"

else:
    print "Sorry, this operating system is not supported"
    sys.exit(1)

#parseUserInput(configFile)
gui = InputGUI(configFile)
gui.guiStart()