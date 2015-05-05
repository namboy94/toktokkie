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

if platform.system() == "Linux":
    #fix pythonpath
    splitPath = sys.argv[0].split("/")
    lengthToCut = len(splitPath[len(splitPath) - 1]) + len(splitPath[len(splitPath) - 2]) + 2
    upperDirectory = sys.argv[0][:-lengthToCut]
    sys.path.append(upperDirectory)
    
    configFile = upperDirectory + "/program/data/config.txt"

else:
    print "Sorry, this operating system is not supported"
    sys.exit(1)

parseUserInput(configFile)
