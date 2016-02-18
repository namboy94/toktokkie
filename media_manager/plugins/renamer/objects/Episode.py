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

from plugins.common.onlineDataGetters.TVDBGetter import TVDBGetter
from plugins.common.fileOps.FileRenamer import FileRenamer


class Episode(object):
    """
    Episode Object, containing important episode info used for renaming and stuff
    """

    def __init__(self, episode_file, episode_number, season_number, show_name):
        """
        Constructor
        :param episode_file: the current episode file path
        :param episode_number: the episode number
        :param season_number: the season number
        :param show_name: the show name
        :return: void
        """
        self.episode_file = episode_file

        self.episode_number = int(episode_number)
        self.season_number = int(season_number)
        self.show_name = show_name

        self.tvdb_getter = TVDBGetter(self.show_name, self.season_number, self.episode_number)

        self.old_name = episode_file.rsplit("/", 1)[1]
        self.tvdb_name = ""
        self.new_name = ""
        self.__generate_tvdb_name__()
        self.__generate_new_name__()

    def rename(self):
        """
        Renames the original file
        :return void
        """
        self.episode_file = FileRenamer.rename_file(self.episode_file, self.new_name)
        
    def print(self):
        """
        Prints the episode object
        :return void
        """
        print("{" + self.episode_file + "," + self.old_name + "," + self.tvdb_name + "," + 
              str(self.episode_number) + "," + str(self.season_number) + "," + self.show_name + "}")

    def __generate_tvdb_name__(self):
        """
        Generates the episode name from the tv database
        :return void
        """
        self.tvdb_name = self.tvdb_getter.find_episode_name()
        illegal_characters = ['/', '\\', '?', '<', '>', ':', '*', '|', "\"", '^']
        for illegal_character in illegal_characters:
            self.tvdb_name = self.tvdb_name.replace(illegal_character, "")
            
    def __generate_new_name__(self):
        """
        Generates the new name of an episode in Plex-conform format.
        :return void
        """
        episode_string = str(self.episode_number)
        season_string = str(self.season_number)
        if len(episode_string) < 2:
            episode_string = "0" + episode_string
        if len(season_string) < 2:
            season_string = "0" + season_string
        self.new_name = self.show_name + " - S" + season_string + "E" + episode_string + " - " + self.tvdb_name
