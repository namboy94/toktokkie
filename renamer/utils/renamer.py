import os
from renamer.objects.Episode import Episode

"""
@author Hermann Krumrey<hermann@krumreyh.com>
class that renames a directory of episodes
@:param directory - the directory to be used
"""
class Renamer(object):

    """
    Constructor
    """
    def __init__(self, directory):
        self.directory = directory
        self.parseDirectory()
        self.confirmed = False

    """
    """
    def parseDirectory(self):

        self.episodes = []

        if not os.path.isdir(self.directory): raise Exception("Not a directory")

        showname = self.directory.rsplit("/", 1)[1]

        seasons = os.listdir(self.directory)
        seasons = self.formatSeasons(seasons)

        for season in seasons:
            qualities = os.listdir(season)
            for quality in qualities:
                qualityDir = season + "/" + quality
                episodes = os.listdir(qualityDir)
                episodes.sort(key=lambda x: x)
                i = 1
                for episode in episodes:
                    episodeDir = qualityDir + "/" + episode
                    episodeNumber = i
                    seasonNumber = season.lower().split("/", 1)[1].split("season ")[1]
                    self.episodes.append(Episode(episodeDir, episodeNumber, seasonNumber, showname))
                    i += 1

    """
    """
    def requestConfirmation(self):
        confirmation = [[], []]
        for episode in self.episodes:
            confirmation[0].append(episode.oldName)
            confirmation[1].append(episode.newName)
        return confirmation

    """
    """
    def confirm(self, confirmation):
        i = 0
        for episode in self.episodes:
            if not episode.oldName == confirmation[0][i] or not episode.newName == confirmation[1][i]:
                return
            i += 1
        self.confirmed = True

    """
    """
    def startRename(self):
        if not self.confirmed: raise Exception("Rename not confirmed")
        for episode in self.episodes:
            os.system("mv \"" + episode.episodeFile + "\" \"" + episode.newEpisodeFile + "\"")


    """
    """
    def formatSeasons(self, seasons):
        newSeasons = []
        for season in seasons:
            if "season" in season.lower():
                newSeasons.append(self.directory + "/" + season)
        return newSeasons