"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

import os
from typing import List

from toktokkie.modules.objects.renamer.Episode import Episode
from toktokkie.modules.objects.renamer.RenamerConfirmation import RenamerConfirmation


class Renamer(object):
    """
    Class that handles the renaming of episode files using thetvdb.com and a naming convention
    that is recognized by most media center software systems:

    Show Name - SXXEXX - Episode Name
    """

    episodes = []
    """
    List of episode objects to be renamed
    """

    confirmed = False
    """
    Flag that is set once the renaming process has been successfully set by the user
    """

    def __init__(self, directory: str) -> None:
        """
        Constructor of the Renamer class. It stores the directory path to the class variable
        reserved for it and parses it.

        :param directory: the directory to be used
        :return: None
        """
        self.episodes = []
        self.parse_directory(directory)

    def parse_directory(self, directory: str) -> None:
        """
        Parses the given directory recursively until it finds .icon directories, which are used as indicators

        :param directory: the directory to parse
        :return: None
        """

        # Check if the directory is a valid directory
        if not os.path.isdir(directory):
            raise NotADirectoryError("Not a directory")  # if not, raise an error

        # List the directories subdirectories
        try:
            children = os.listdir(directory)
        except PermissionError:
            # If we don't have read permissions for this directory, skip this directory
            return

        # Check if one of the subdirectories is .icons
        if ".icons" in children:
            # If yes, add the content to the list of episodes
            self.add_directory_content(directory)
        else:
            # Else parse every subdirectory like the original directory
            for child in children:
                child_path = os.path.join(directory, child)
                if os.path.isdir(child_path):  # Check if this is a directory
                    self.parse_directory(child_path)  # Recurse

    def add_directory_content(self, directory: str) -> None:
        """
        Add the content of a directory to the Episode list

        :param directory: the directory to be parsed for episode content
        :return: None
        """

        # Find out the show name
        show_name = os.path.basename(directory)

        # get a list of all subdirectory's names
        seasons = os.listdir(directory)

        # A list to store special seasons (like OVAs, Movies, etc.)
        specials = []

        # Iterate over each season
        for season in seasons:

            # Calculate the path to the subdirectory
            season_path = os.path.join(directory, season)

            # If the directory's name is .icons or is not a directory, skip this subdirectory
            # and continue with the next
            if season == ".icons" or not os.path.isdir(season_path):
                continue

            # If the season directory's name does not start with "Season", add this subdirectory
            # to the list of special seasons
            if not season.lower().startswith("season"):
                specials.append(season_path)
            else:
                # Calculate the season number
                season_number = int(season.lower().split("season ")[1])
                # Add Episode objects to the Episode list
                self.add_season_to_episodes(season_path, season_number, show_name)

        # Add the special episodes to the Episode list
        self.add_specials_to_episodes(specials, show_name)

    def add_season_to_episodes(self, season_directory: str, season_number: int, show_name: str) -> None:
        """
        Adds a 'season' subdirectory's content to the Episode List

        :param season_directory: The season directory path to be parsed
        :param season_number:  The season number of the season to be parsed
        :param show_name: The show name associated wihh this season
        :return: None
        """

        # get the episode file names and sort them alphabetically
        episodes = os.listdir(season_directory)
        episodes.sort(key=lambda x: x)

        # Counter variable for the episode number
        episode_number = 1

        # loop through all episodes
        for episode in episodes:
            # We don't want to rename openings and endings, marked with 'OP' or 'ED' with a space afterwards
            if episode.startswith("OP ") or episode.startswith("ED "):
                continue

            # Generate the episode path
            episode_path = os.path.join(season_directory, episode)
            # Add Episode object to list of Episodes
            self.episodes.append(Episode(episode_path, episode_number, season_number, show_name))
            episode_number += 1  # Increment the episode counter

    # noinspection PyTypeChecker
    def add_specials_to_episodes(self, list_of_special_directories: List[str], show_name: str) -> None:
        """
        Adds all special episodes like OVAs, Movies, etc. to the Episode list

        :param list_of_special_directories: List of paths to the special season subdirectories
        :param show_name: The show name associated with these special seasons
        :return: None
        """

        # The special episodes are stored in a list
        special_episodes = []

        # Loop through all special seasons to get the episode files
        for special_season in list_of_special_directories:
            for episode in os.listdir(special_season):
                special_episodes.append(os.path.join(special_season, episode))

        # Sort by filename
        special_episodes.sort(key=lambda x: os.path.basename(x))

        # Add episodes to the Episode list as Episode objects
        special_episode_number = 1  # Episode Counter
        for special_episode in special_episodes:
            # Use season number 0 to specify that this is part of a special season
            self.episodes.append(Episode(special_episode, special_episode_number, 0, show_name))  # Add to List
            special_episode_number += 1  # Increment Counter

    def request_confirmation(self) -> List[RenamerConfirmation]:
        """
        Request for the renaming confirmation objects.

        :return: the confirmation prompt as list of RenamerConfirmation objects
        """
        confirmation = []  # Initialize list
        for episode in self.episodes:  # Loop through all episodes
            confirmation.append(RenamerConfirmation(episode))
        return confirmation

    def confirm(self, confirmation: List[RenamerConfirmation]) -> None:
        """
        Confirms the rename process by getting the previously returned list of RenamerConfirmations
        and checking their status.
        Only confirmed objects will be put back into the episode list

        :param confirmation: the confirmation list
        :return None
        """
        if len(self.episodes) != len(confirmation):
            self.confirmed = False
            return

        self.episodes = []

        for item in confirmation:
            if item.confirmed:
                self.episodes.append(item.episode)

        self.confirmed = True

    def start_rename(self, noconfirm: bool = False) -> None:
        """
        Renames all episodes in the Episode List

        :param noconfirm: Can be used to bypass confirming.
        :return: None
        """
        # If the result has not been confirmed before, raise an Error.
        # Do not raise an error if the noconfirm flag has been set though.
        if not self.confirmed and not noconfirm:
            raise AssertionError("Rename not confirmed")

        # Rename all episodes
        for episode in self.episodes:
            episode.rename()
