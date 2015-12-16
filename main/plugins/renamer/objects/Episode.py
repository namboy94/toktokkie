import tvdb_api
from plugins.common.onlineDataGetters.TVDBGetter import TVDBGetter
from plugins.common.fileOps.FileRenamer import FileRenamer

"""
Episode Object
"""
class Episode(object):

    """
    Constructor
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

        FileRenamer.renameFile(self.episodeFile, self.newName)

    """
    Prints the episode object
    """
    def print(self):

        print("{" + self.episodeFile + "," + self.oldName + "," + self.tvdbName + ","
              + str(self.episodeNumber) + "," + str(self.seasonNumber) + "," + self.showName + "}")

    """
    """
    def __generateTVDBName__(self):

        self.tvdbName = self.tvdbGetter.findEpisodeName()

    """
    """
    def __generateNewName__(self):

        episodeString = str(self.episodeNumber)
        seasonString = str(self.seasonNumber)
        if len(episodeString) < 2: episodeString = "0" + episodeString
        if len(seasonString) < 2: seasonString = "0" + seasonString
        self.newName = self.showName + " - S" + seasonString + "E" + episodeString + " - " + self.tvdbName

