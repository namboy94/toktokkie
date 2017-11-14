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