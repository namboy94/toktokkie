'''
userInputParser
parses the user's input

Created on Apr 25, 2015
Modified on May 2, 2015

@author Hermann Krumrey
@version 0.2
'''

#imports
import sys
import os
from program.objects.Episode import Episode

"""
parseUserInput
parses the user's input.
"""
def parseUserInput(configFile):
    
    #illegal characters list for ensuring compatibility on Windows systems
    #theoretically, any character can be autoremoved with this
    illegalCharacters = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
    
    #Asks for show name and replaces all illegal characters in the show's name with a whitespace
    showName = raw_input("Please enter the show's name:   ")
    for illegalCharacter in illegalCharacters:
        if showName.contains(illegalCharacter):
            showName = showName.replace(illegalCharacter, "")
    
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
    print "%s to be used.    " % (defaultDirectory)
    userInput = raw_input("")
    if userInput == "":
        workingDirectory = defaultDirectory
        if not os.path.isdir(workingDirectory):
            print "Invalid directory in config file. Please fix."
            sys.exit(1)
    else:
        workingDirectory = userInput
        if not workingDirectory.endswith("/"):
            workingDirectory = workingDirectory + "/"
        if not os.path.isdir(workingDirectory):
            print "Invalid Directory input by luser. Please fix (the user)."
            sys.exit(1)
        openedWorkingConfigFile = open(configFile, "w")
        openedWorkingConfigFile.close()
        openedWorkingConfigFile = open(configFile, "a")
        openedWorkingConfigFile.write(workingDirectory)
        openedWorkingConfigFile.close()
    
    #Sorts the list of files in the directory
    directoryContent = os.listdir(workingDirectory)
    directoryContent.sort(key=lambda x: x)
    
    #checks if the amount of files in workingDirectory equals the amount of episodes
    #input at the beginning of the method. 
    if len(directoryContent) != episodeAmount:
        print "Not the same amount of episodes in the directory as previously input"
        sys.exit(1)
    
    #Initializes all Episode objects and appends them to a list
    episodeList = []
    currentEpisode = episodeNo
    nameIndex = 0
    
    #Appending to list
    while currentEpisode <= episodeAmountTotal:
        episodeName = directoryContent[nameIndex]
        episodeObject = Episode(episodeName, workingDirectory, currentEpisode, showName, seasonNo)
        episodeList.append(episodeObject)
    
    #Prompts for user input - new episode names
    for episode in episodeList:
        print "Please enter the new name for episode %s - %s" % (episode.episodeNumber, episode.fileName)
        renameInput = raw_input("")
        episode.setRenameName(renameInput, illegalCharacters)
    
    #Prints all changes to be done:
    for episode in episodeList:
        episode.confirmationPrint()
    
    #for episode in episodeList:
    #    episode.rename()