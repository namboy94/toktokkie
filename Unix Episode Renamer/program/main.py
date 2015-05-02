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
from program.utils.userInputParser import parseUserInput

#fix pythonpath
splitPath = sys.argv[0].split("/")
lengthToCut = len(splitPath[len(splitPath) - 1]) + len(splitPath[len(splitPath) - 2]) + 2
upperDirectory = sys.argv[0][:-lengthToCut]
sys.path.append(upperDirectory)

configFile = upperDirectory + "/program/data/config.txt"

parseUserInput(configFile)
