"""
LICENSE:

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

LICENSE
"""

# imports
import os
from subprocess import Popen
from typing import Tuple

try:
    from plugins.batchdownloadmanager.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
    from plugins.batchdownloadmanager.downloaders.TwistedDownloader import TwistedDownloader
    from plugins.batchdownloadmanager.searchengines.IntelGetter import IntelGetter
    from plugins.batchdownloadmanager.searchengines.IxIRCGetter import IxIRCGetter
    from plugins.batchdownloadmanager.searchengines.NIBLGetter import NIBLGetter
    from plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from plugins.common.fileops.FileMover import FileMover
except ImportError:
    from media_manager.plugins.batchdownloadmanager.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
    from media_manager.plugins.batchdownloadmanager.downloaders.TwistedDownloader import TwistedDownloader
    from media_manager.plugins.batchdownloadmanager.searchengines.IntelGetter import IntelGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.IxIRCGetter import IxIRCGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.NIBLGetter import NIBLGetter
    from media_manager.plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from media_manager.plugins.common.fileops.FileMover import FileMover


class BatchDownloadManager(object):
    """
    A class containing the functionality of te Batch Download Manager Plugin.
    """

    @staticmethod
    def conduct_xdcc_search(search_engine, search_term):
        """
        Conducts the XDCC search
        :param search_engine: the search engine to be used
        :param search_term: the search term
        :return: the search result
        """
        if search_engine == "NIBL.co.uk":
            search_result = NIBLGetter(search_term).search()
        elif search_engine == "intel.haruhichan.com":
            search_result = IntelGetter(search_term).search()
        elif search_engine == "ixIRC.com":
            search_result = IxIRCGetter(search_term).search()
        else:
            raise NotImplementedError("The selected search engine is not implemented")
        return search_result

    @staticmethod
    def get_icon(path, folder_icon_directory, icon_file):
        """
        Gets the icons specified by the user with either wget or cp
        :param path: the path to the icon file
        :param folder_icon_directory: the folder icon directory
        :param icon_file: the icon file to which the icon will be saved to
        :return void
        """
        if os.path.isfile(path):
            if not path == folder_icon_directory + icon_file:
                if os.path.isfile(folder_icon_directory + icon_file):
                    Popen(["rm", folder_icon_directory + icon_file]).wait()
                Popen(["cp", path, folder_icon_directory + icon_file]).wait()
        else:
            before = os.listdir(os.getcwd())
            Popen(["wget", path]).wait()
            after = os.listdir(os.getcwd())
            new_file = ""
            for file in after:
                if file not in before:
                    new_file = file
                    break
            Popen(["mv", new_file, folder_icon_directory + icon_file]).wait()

    @staticmethod
    def prepare(directory, show, season_string, first_episode_string, main_icon, secondary_icon, iconizer_method):
        """
        Prepares the download
        :param iconizer_method: the iconizer method to be used
        :param secondary_icon: the secondary icon
        :param main_icon: the main icon
        :param first_episode_string: the first episode as string
        :param season_string: the season number/name as string
        :param show: the show name
        :param directory: the directory of the show
        :return: {directory: the original directory,
                  show: the show name,
                  season: the season number,
                  first_episode: the first episode number,
                  special: if it's special,
                  new_directory: and the new directory}
        """
        if os.path.isdir(directory):
            update = True
        else:
            update = False

        if not show:
            return "No show name specified", ""

        if not season_string:
            return "No Season number specified", ""

        try:
            season = int(season_string)
            special = False
        except ValueError:
            season = season_string
            special = True

        if special:
            new_directory = os.path.join(directory, str(season))
        else:
            new_directory = os.path.join(directory, "Season " + str(season))

        if not update:
            os.makedirs(directory)
            if not os.path.isdir(directory):
                return "Error creating directory", "Was a valid directory string entered?"
            os.makedirs(os.path.join(directory, ".icons"))

        season_update = False
        if update and os.path.isdir(new_directory):
            season_update = True

        if not season_update:
            os.makedirs(new_directory)

        episodes = os.listdir(new_directory)
        first_episode = len(episodes) + 1

        if main_icon:
            if BatchDownloadManager.get_icon(main_icon, os.path.join(directory, ".icons"), "media_manager.png")\
                    == "error":
                return "Error retrieving image from source", ""
        if secondary_icon:
            if BatchDownloadManager.get_icon(secondary_icon, os.path.join(directory, ".icons"),
                                             os.path.dirname(new_directory) + ".png") == "error":
                return "Error retrieving image from source", ""

        if main_icon or secondary_icon:
            DeepIconizer(directory, iconizer_method).iconize()

        if first_episode_string:
            try:
                first_episode = int(first_episode_string)
            except ValueError:
                return "Not a valid episode number", ""

        return {"directory": directory, "show": show, "season": season, "first_episode": first_episode,
                "special": special, "new_directory": new_directory}

    @staticmethod
    def start_download_process(preparation, downloader, packs, auto_rename, progress_struct):
        """
        Starts the XDCC download
        :param preparation: the preparation dictionary created beforehand
        :param downloader: the downloader to use
        :param packs: the packs to download
        :param auto_rename: bool that determines if the files will be auto-renamed
        :param progress_struct: A ProgressStruct object to keep track of the download progress
        :return: void
        """
        files = []
        if downloader == "Hexchat Plugin":
            if auto_rename and not preparation["special"]:
                HexChatPluginDownloader(packs,
                                                progress_struct,
                                                preparation["show"],
                                                preparation["first_episode"],
                                                preparation["season"]).download_loop()
            else:
                HexChatPluginDownloader(packs, progress_struct).download_loop()

        elif downloader == "Twisted":
            if auto_rename and not preparation["special"]:
                TwistedDownloader(packs,
                                          progress_struct,
                                          preparation["new_directory"],
                                          preparation["show"],
                                          preparation["first_episode"],
                                          preparation["season"]).download_loop()
            else:
                TwistedDownloader(packs, progress_struct, preparation["new_directory"]).download_loop()

    @staticmethod
    def analyse_show_directory(directory: str) -> Tuple[str, str, str, str, str]:
        """
        Method that calculates the default values for a show directory

        :param directory: the directory to be checked
        :return: the show name, the highest season, the amount of episodes, the main icon path and the
                    secondary icon path as a five-part tuple
        """
        show_name = os.path.basename(directory)  # Get the show name from a directory

        # These are the default values if the directory does not exist
        highest_season = 1  # Set highest season to 1
        episode_amount = 1  # Set amount of episodes to 1
        main_icon = ""  # Set main icon location to ""
        second_icon = ""  # Set secondary icon location to ""

        if os.path.isdir(directory):  # If the directory already exists, check its content
            highest_season = 1
            # Check how many season subdirectories there are
            while os.path.isdir(os.path.join(directory, "Season " + str(highest_season + 1))):
                highest_season += 1

            # Now check how many episodes are inside the last season folder
            if os.path.isdir(os.path.join(directory, "Season " + str(highest_season))):
                children = os.listdir(os.path.join(directory, "Season " + str(highest_season)))
                episode_amount = len(children) + 1

            # Check for icons:

        if os.path.isfile(os.path.join(directory, ".icons", "main.png")):
            main_icon = os.path.join(directory, ".icons", "main.png")
        if os.path.isfile(os.path.join(directory, ".icons", "Season " + str(highest_season) + ".png")):
            secondary_icon = os.path.join(directory, ".icons", "Season " + str(highest_season) + ".png")

        return show_name, str(highest_season), str(episode_amount), main_icon, second_icon
