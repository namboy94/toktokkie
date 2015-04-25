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

"""
parseUserInput
parses the user's input.
"""
def parseUserInput():
    
    showName = raw_input("Please enter the show's name:   ")

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
        
    