'''
Episode
Models an episode

Created on May 2, 2015
Created on May 2, 2015

@author Hermann Krumrey
@version 0.1
'''

#imports
import os

'''
Episode
The class that models the episode
'''
class Episode(object):
    
    '''
    Constructor
    Constructs a new episode object
    @param name - the name of the episode
    @param location - the directory of the file
    @param episodeNumber - the number of the episode (int)
    @param series - the name of the series this episode belongs to
    @param season - the number of the season this episode belongs to (string)
    '''
    def __init__(self, name, location, episodeNumber, series, season):
                    
        self.fileName = name
        self.parentPath = location
        self.filePath = location + name
        self.episodeName = os.path.splitext(self.filePath)[0]
        self.fileExtension = os.path.splitext(self.filePath)[1]
        self.series = series
        self.season = season
        
        if episodeNumber < 10:
            self.episodeNumber = "0" + str(episodeNumber)
        else:
            self.episodeNumber = str(episodeNumber)
        
    """
    rename
    Renames the physical reference of this object to a new file name.
    This does not change the object's properties.
    """
    def rename(self):
        
        commandString = "mv \"" + self.filePath + "\" \"" + self.renameFile + "\""
        os.system(commandString)
        
    """
    setRenameName
    sets two 'self variables, that store the new episode name's name
    and the resulting filepath
    @param renameNameInput - the new name of the episode
    @param illegalCharacters - list of illegal characters
    """
    def setRenameName(self, renameNameInput, illegalCharacters):
        
        for illegalCharacter in illegalCharacters:
            if illegalCharacter in renameNameInput:
                renameNameInput = renameNameInput.replace(illegalCharacter, "")
        
        if renameNameInput.endswith("!") or renameNameInput.endswith("."):
            renameNameInput = renameNameInput + " "
            
        self.renameName = renameNameInput
        
        renameFile = self.filePath + self.series + " - S" + self.season + "E" + self.episodeNumber
        renameFile = renameFile + " - " + renameNameInput + self.fileExtension
        self.renameFile = renameFile
        
    """
    confirmationPrint
    prints a summary of the rename method's future processes.
    """
    def confirmationPrint(self):
        print "Episode    %s" % (self.episodeNumber)
        print "OLD:       %s" % (self.episodeName)
        print "NEW        %s\n" % (self.renameName)