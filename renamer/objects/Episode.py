import tvdb_api

class Episode(object):

    def __init__(self, episodeFile, episodeNumber, seasonNumber, showName):
        self.episodeFile = episodeFile
        self.episodeNumber = int(episodeNumber)
        self.seasonNumber = int(seasonNumber)
        self.showName = showName
        self.oldName = episodeFile.rsplit("/", 1)[1]
        self.tvdbName = ""
        self.generateTVDBName()
        self.newEpisodeFile = episodeFile.rsplit(self.oldName)[0] + self.tvdbName

    def generateTVDBName(self):

        tvdb = tvdb_api.Tvdb()
        self.print()
        episodeInfo = tvdb[self.showName][self.seasonNumber][self.episodeNumber]
        episodeName = episodeInfo['episodename']
        self.tvdbName = episodeName

    def print(self):

        print("{" + self.episodeFile + "," + self.oldName + "," + self.tvdbName + ","
              + str(self.episodeNumber) + "," + str(self.seasonNumber) + "," + self.showName + "}")