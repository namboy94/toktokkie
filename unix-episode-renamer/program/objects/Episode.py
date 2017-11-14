"""
Copyright 2015-2017 Hermann Krumrey

This file is part of unix-episode-renamer.

unix-episode-renamer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

unix-episode-renamer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with unix-episode-renamer.  If not, see <http://www.gnu.org/licenses/>.
"""

'''
Episode
Models an episode

Created on May 2, 2015
Created on May 2, 2015

@author Hermann Krumrey
@version 1.0
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
        
        renameFile = self.parentPath + self.series + " - S" + self.season + "E" + self.episodeNumber
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