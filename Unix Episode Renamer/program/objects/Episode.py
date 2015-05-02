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
    '''
    def __init__(self, name, location, episodeNumber, series, season):
        self.fileName = name
        self.parentPath = location
        self.filePath = location + name
        self.episodeName = os.path.splitext(self.filePath)[0]
        self.episodeNumber = episodeNumber
        self.series = series
        self.season = season
        
    def rename(self, newFileName):
        newFilePath = self.parentPath + newFileName
        commandString = "mv \"" + self.filePath + "\" \"" + newFilePath + "\""
        os.system(commandString)