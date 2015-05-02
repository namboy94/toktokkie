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
    @param episodeNumber - the number of the episode
    @param series - the name of the series this episode belongs to
    @param season - the number of the season this episode belongs to
    @param illegalCharacters - list of illegal characters
    '''
    def __init__(self, name, location, episodeNumber, series, season):
                    
        self.fileName = name
        self.parentPath = location
        self.filePath = location + name
        self.episodeName = os.path.splitext(self.filePath)[0]
        self.episodeNumber = episodeNumber
        self.series = series
        self.season = season
        
    """
    rename
    Renames the physical reference of this object to a new file name.
    This does not change the object's properties.
    @param newFileName - the new name of the file
    """
    def rename(self, newFileName, illegalCharacters):
        
        for illegalCharacter in illegalCharacters:
            if newFileName.contains(illegalCharacter):
                newFileName = newFileName.replace(illegalCharacter, "")
        
        if newFileName.endswith("!") or newFileName.endswith("."):
            newFileName = newFileName + " "
        
        newFilePath = self.parentPath + newFileName + os.path.splitext(self.filepath)[1]
        
        commandString = "mv \"" + self.filePath + "\" \"" + newFilePath + "\""
        os.system(commandString)