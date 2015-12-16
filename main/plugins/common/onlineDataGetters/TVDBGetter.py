import tvdb_api
from plugins.common.fileOps.FileRenamer import FileRenamer

"""
the TVDBGetter class
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class TVDBGetter(object):

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, tvshow, season, episode):
        self.tvshow = tvshow
        self.season = season
        self.episode = episode

    """
    Finds the episode name and returns it as string
    """
    def findEpisodeName(self):
        return self.__getEpisodeName__()

    """
    Finds the episode name and then renames a file.
    """
    def renameEpisodeFile(self, file):
        newName = self.__getEpisodeName__()
        if newName:
            FileRenamer.renameFile(file, newName)

    """
    Searches for the episode name
    """
    def __getEpisodeName__(self):
        try:
            tvdb = tvdb_api.Tvdb()
            episodeInfo = tvdb[self.tvshow][self.season][self.episode]
            episodeName = episodeInfo['episodename']
            return episodeName
        except: return ""