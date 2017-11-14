"""
Copyright 2015-2017 Hermann Krumrey

This file is part of tvdb-episode-renamer.

tvdb-episode-renamer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tvdb-episode-renamer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with tvdb-episode-renamer.  If not, see <http://www.gnu.org/licenses/>.
"""

import tvdb_api

class Episode(object):

    def __init__(self, episodeFile, episodeNumber, seasonNumber, showName):
        self.episodeFile = episodeFile
        self.episodeNumber = int(episodeNumber)
        self.seasonNumber = int(seasonNumber)
        self.showName = showName
        self.oldName = episodeFile.rsplit("/", 1)[1]
        self.tvdbName = ""
        self.newName = ""
        self.generateTVDBName()
        self.generateNewName()
        self.newEpisodeFile = episodeFile.rsplit(self.oldName)[0] + self.newName

    def generateTVDBName(self):

        tvdb = tvdb_api.Tvdb()
        episodeInfo = tvdb[self.showName][self.seasonNumber][self.episodeNumber]
        episodeName = episodeInfo['episodename']
        self.tvdbName = episodeName

    def generateNewName(self):

        episodeString = str(self.episodeNumber)
        seasonString = str(self.seasonNumber)
        if len(episodeString) < 2: episodeString = "0" + episodeString
        if len(seasonString) < 2: seasonString = "0" + seasonString
        self.newName = self.showName + " - S" + seasonString + "E" + episodeString + " - " + self.tvdbName

    def print(self):

        print("{" + self.episodeFile + "," + self.oldName + "," + self.tvdbName + ","
              + str(self.episodeNumber) + "," + str(self.seasonNumber) + "," + self.showName + "}")