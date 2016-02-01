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