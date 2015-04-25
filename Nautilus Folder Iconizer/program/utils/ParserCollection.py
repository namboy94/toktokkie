'''
ParserCollection
collection of parsing methods.

Created on Apr 25, 2015
Modified on Apr 25, 2015

@author Hermann Krumrey
@version 0.1
'''

#imports
import os

"""
directoryChangeParser
prompts for a change of the directory to be iconized
@param configFileLocation - the location of the configuration file
"""
def directoryChangeParser(configFileLocation):
    configFile = open(configFileLocation,"r")
    directoryPath = configFile.readline()
    
    #Asks for a yes/no prompt
    print "Current active directory is %s" % (directoryPath)
    print "Do you want to change the directory? (y/n)"
    yesNoPrompt = True
    while yesNoPrompt is True:
        answer = raw_input()
        if answer == "y":
            yesNoPrompt = False
            change = True
        elif answer == "n":
            yesNoPrompt = False
            change = False
        else:
            print "Input was not understood. Please enter \"y\" or \"n\":"
    
    #change the directory
    if change is True:
        newDirectory = raw_input("Please enter the new directory:")
        directoryPrompt = True
        while directoryPrompt == True:
            newDirectory = raw_input()
            if not newDirectory.endswith("/"):
                newDirectory = newDirectory + "/"
            
            if os.path.isdir(newDirectory):
                directoryPrompt = False
            else:
                print "This is not a valid directory, please try again."
        configFile.close()
        configFile = open(configFileLocation,"w")
        configFile.close()
        configFile = open(configFileLocation,"a")
        configFile.write(newDirectory)
        configFile.close()