"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a progam that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.
"""

from plugins.common.onlineDataGetters.TVDBGetter import TVDBGetter
from plugins.common.fileOps.FileRenamer import FileRenamer

"""
Episode Object, containing important episode info used for renaming and stuff
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class Episode(object):

    """
    Constructor
    @:param episodeFile - the current episode file path
    @:param episodeNumber - the episode number
    @:param seasonNumber - the season number
    @:param showName - the show name
    """
    def __init__(self, episodeFile, episodeNumber, seasonNumber, showName):
        self.episodeFile = episodeFile

        self.episodeNumber = int(episodeNumber)
        self.seasonNumber = int(seasonNumber)
        self.showName = showName

        self.tvdbGetter = TVDBGetter(self.showName, self.seasonNumber, self.episodeNumber)

        self.oldName = episodeFile.rsplit("/", 1)[1]
        self.tvdbName = ""
        self.newName = ""
        self.__generateTVDBName__()
        self.__generateNewName__()

    """
    Renames the original file
    """
    def rename(self):

        self.episodeFile = FileRenamer.renameFile(self.episodeFile, self.newName)

    """
    Prints the episode object
    """
    def print(self):

        print("{" + self.episodeFile + "," + self.oldName + "," + self.tvdbName + ","
              + str(self.episodeNumber) + "," + str(self.seasonNumber) + "," + self.showName + "}")

    """
    Geerates the episode name from the tv database
    """
    def __generateTVDBName__(self):

        self.tvdbName = self.tvdbGetter.findEpisodeName()
        illegalCharacters = ['/', '\\', '?', '<', '>', ':', '*', '|', "\"", '^']
        for illegalCharacter in illegalCharacters:
            self.tvdbName = self.tvdbName.replace(illegalCharacter, "")

    """
    Generates the new name of an episode in Plex-conform format.
    """
    def __generateNewName__(self):

        episodeString = str(self.episodeNumber)
        seasonString = str(self.seasonNumber)
        if len(episodeString) < 2: episodeString = "0" + episodeString
        if len(seasonString) < 2: seasonString = "0" + seasonString
        self.newName = self.showName + " - S" + seasonString + "E" + episodeString + " - " + self.tvdbName

