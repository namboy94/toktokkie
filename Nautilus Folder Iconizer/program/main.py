'''
main
The main program that ties the whole project together

Created on Apr 25, 2015
Modified on Apr 25, 2015

@author Hermann Krumrey
@version 1.2
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
#    sys.exit("This program needs root priviliges.")

configFileLocation = upperDirectory + "/program/data/config.txt"
warningFileLocation = upperDirectory + "/program/data/warnings.txt"
directoryChangeParser(configFileLocation)
activeDirectory = getActiveDirectory(configFileLocation)

iconParser(activeDirectory, warningFileLocation)