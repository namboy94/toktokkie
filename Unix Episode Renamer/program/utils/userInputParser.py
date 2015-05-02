'''
userInputParser
parses the user's input

Created on Apr 25, 2015
Modified on Apr 25, 2015

@author Hermann Krumrey
@version 0.1
'''

#imports
import sys
import os

"""
parseUserInput
parses the user's input.
"""
def parseUserInput(configFile):
    
    showName = raw_input("Please enter the show's name:   ")

    #Asks for number of episodes, the first episode number and the season number.
    try:
        episodeNo = int(raw_input("Please enter the first episode's number   "))
        episodeAmountTotal = int(raw_input("Please enter the total amount of episodes   "))
        episodeAmount = episodeAmountTotal - (episodeNo - 1)
        if episodeAmount < 0:
            #Exits program because of negative amount of episodes
            print "Invalid amount of episodes, the program will now halt."
            sys.exit(1)
        seasonNo = int(raw_input("Please enter the show's season number   "))
        if seasonNo < 0:
            #Exits program because of negative season value
            print "Can't use a negative season number. The program will now halt."
            sys.exit(1)
        if seasonNo < 10:
            seasonString = "0" + str(seasonNo)
        else:
            seasonString = str(seasonNo)
    except TypeError:
        print "Please enter valid integer values for season number, episode number and amount of episodes"
        sys.exit(1)
        
    #asks for the directory of the files to be renamed (default value is from configFile)
    openedWorkingConfigFile = open(configFile, "r")
    defaultDirectory = openedWorkingConfigFile.readline()
    openedWorkingConfigFile.close()
    print "Please enter the directory to be used. A blank input will result in"
    print "%s to be used." % (defaultDirectory)
    userInput = raw_input("")
    if userInput == "":
        workingDirectory = defaultDirectory
    else:
        workingDirectory = userInput
        if not workingDirectory.endswith("/"):
            workingDirectory = workingDirectory + "/"
        if not os.path.isdir(workingDirectory):
            print "Invalid Directory"
            sys.exit(1)
        openedWorkingConfigFile = open(configFile, "w")
        openedWorkingConfigFile.close()
        openedWorkingConfigFile = open(configFile, "a")
        openedWorkingConfigFile.write(workingDirectory)
        openedWorkingConfigFile.close()
    