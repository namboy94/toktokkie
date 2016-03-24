"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
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

try:
    from plugins.common.fileops.FileRenamer import FileRenamer
except ImportError:
    from media_manager.plugins.common.fileops.FileRenamer import FileRenamer


class TVDBGetter(object):
    """
    the TVDBGetter class
    """

    def __init__(self, tv_show, season, episode):
        """
        Constructor
        :param tv_show: the tv show's name
        :param season: the season to search
        :param episode: the episode to search
        :return: void
        """
        self.tv_show = tv_show
        self.season = season
        self.episode = episode

    def find_episode_name(self):
        """
        Finds the episode name and returns it as string
        :return the episode name
        """
        return self.__get_episode_name__()

    def rename_episode_file(self, file):
        """
        Finds the episode name and then renames a file.
        :param file: the file top rename
        :return: void
        """
        new_name = self.__get_episode_name__()
        if new_name:
            FileRenamer.rename_file(file, new_name)

    def __get_episode_name__(self):
        """
        Searches for the episode name
        :return: the episode name, or "" if an exception occured
        """
        try:
            tvdb = tvdb_api.Tvdb()
            episode_info = tvdb[self.tv_show][self.season][self.episode]
            episode_name = episode_info['episodename']
            return episode_name
        except Exception as e:
            print("Check which kind of Exception this is")
            print(str(e))
            return ""
