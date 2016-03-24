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

import os

try:
    from plugins.renamer.objects.Episode import Episode
except ImportError:
    from media_manager.plugins.renamer.objects.Episode import Episode


class Renamer(object):
    """
    Class that renames a directory of episodes
    """

    def __init__(self, directory):
        """
        Constructor
        :param directory: the directory to be used
        """
        self.episodes = []
        self.directory = directory
        self.parse_directory()
        self.confirmed = False

    def parse_directory(self):
        """
        Parses the given directory
        :return: void
        """

        if not os.path.isdir(self.directory):
            raise Exception("Not a directory")

        show_name = os.path.basename(self.directory)

        seasons = os.listdir(self.directory)
        seasons = self.format_seasons(seasons)

        for season in seasons:
            episodes = os.listdir(season)
            episodes.sort(key=lambda x: x)
            i = 1
            for episode in episodes:
                episode_dir = os.path.join(season, episode)
                episode_number = i
                season_number = os.path.basename(season).lower().split("season ")[1]
                self.episodes.append(Episode(episode_dir, episode_number, season_number, show_name))
                i += 1

    def request_confirmation(self):
        """
        Request for user confirmation
        :return the confirmation prompt as double list thingy
        """
        confirmation = [[], []]
        for episode in self.episodes:
            confirmation[0].append(episode.old_name)
            confirmation[1].append(episode.new_name)
        return confirmation

    def confirm(self, confirmation):
        """
        Confirms the rename process
        :param confirmation: to check the confirmation once more
        :return void
        """
        i = 0
        for episode in self.episodes:
            if not episode.old_name == confirmation[0][i] or not episode.new_name == confirmation[1][i]:
                return
            i += 1
        self.confirmed = True

    def start_rename(self):
        """
        Starts the renaming process
        """
        if not self.confirmed:
            raise Exception("Rename not confirmed")
        for episode in self.episodes:
            episode.rename()

    def format_seasons(self, seasons):
        """
        Formats the seasons
        :param seasons: the seasons to be formatted
        :return: the new seasons
        """
        new_seasons = []
        for season in seasons:
            if "season" in season.lower():
                new_seasons.append(os.path.join(self.directory, season))
        return new_seasons
