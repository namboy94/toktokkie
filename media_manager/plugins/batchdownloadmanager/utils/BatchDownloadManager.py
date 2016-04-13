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
import shutil
import urllib.request
import urllib.error
from subprocess import Popen
from typing import Tuple, List, Dict

try:
    from plugins.batchdownloadmanager.searchengines.SearchEngineManager import SearchEngineManager
    from plugins.batchdownloadmanager.downloaders.DownloaderManager import DownloaderManager
    from plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack
    from plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from plugins.common.fileops.FileMover import FileMover
except ImportError:
    from media_manager.plugins.batchdownloadmanager.searchengines.SearchEngineManager import SearchEngineManager
    from media_manager.plugins.batchdownloadmanager.downloaders.DownloaderManager import DownloaderManager
    from media_manager.plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack
    from media_manager.plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from media_manager.plugins.common.fileops.FileMover import FileMover


class BatchDownloadManager(object):
    """
    A class containing the functionality of the Batch Download Manager Plugin. From both a CLI
    and GUI environment.
    """

    @staticmethod
    def conduct_xdcc_search(search_engine: str, search_term: str) -> List[XDCCPack]:
        """
        Conducts the XDCC search using the selected search engine and search term

        :param search_engine: the search engine to be used
        :param search_term: the search term
        :return: the search results as a list of XDCCPack objects
        """
        # Get the selected search engine
        selected_search_engine = SearchEngineManager.get_search_engine_from_string(search_engine)
        # and conduct a search
        # noinspection PyCallingNonCallable
        return selected_search_engine(search_term).search()

    @staticmethod
    def get_icon(path: str, folder_icon_directory: str, icon_file: str) -> str:
        """
        Gets the icons specified by the user with either wget or the local file system
        DOWNLOADING VIA WGET CURRENTLY ONLY WORKS ON LINUX OPERATING SYSTEMS!!!

        :param path: the path to the icon file - either a URL or a local file path
        :param folder_icon_directory: the folder icon directory
        :param icon_file: the icon file to which the icon will be saved to
        :return: A status message
        """
        # If the specified path is a file, not a URL
        if os.path.isfile(path):
            # if the file is not already the one in the folder icon directory
            if not path == os.path.join(folder_icon_directory, icon_file):
                # Remove previous icon file if it exists
                if os.path.isfile(os.path.join(folder_icon_directory, icon_file)):
                    os.remove(os.path.join(folder_icon_directory, icon_file))
                # Copy the icon file to the folder icon directory
                shutil.copyfile(path, os.path.join(folder_icon_directory, icon_file))
        else:
            # Download file via http url
            try:
                urllib.request.urlretrieve(path, os.path.join(folder_icon_directory, icon_file))
            except urllib.error.HTTPError:
                # If file could not be downloaded, return error string
                return "error"

        # If all went well, return "ok" to let the caller know that everything went OK.
        return "ok"

    @staticmethod
    def prepare(directory: str, show: str, season_string: str, first_episode_string: str,
                main_icon: str, secondary_icon: str, iconizer_method: str) \
            -> Dict[str, type]:
        """
        Creates a preparation tuple for the downloader, parsing important information
        and checking for errors

        :param directory: the directory of the show
        :param show: the show name
        :param season_string: the season number/name as string
        :param first_episode_string: the first episode as string
        :param main_icon: the main icon
        :param secondary_icon: the secondary icon
        :param iconizer_method: the iconizer method to be used

        :return: {directory: the original directory,
                  show: the show name,
                  season: the season number,
                  first_episode: the first episode number,
                  special: if it's special,
                  target_directory: and the target directory}
                  OR
                  dictionary with two elements containing an error message
        """
        if os.path.isdir(directory):
            update = True
        else:
            update = False

        if not show:
            return {"error_title": "No show name specified", "error_text": ""}

        if not season_string:
            return {"error_title": "No Season number specified", "error_text": ""}

        try:
            season = int(season_string)
            special = False
        except ValueError:
            season = season_string
            special = True

        if special:
            target_directory = os.path.join(directory, str(season))
        else:
            target_directory = os.path.join(directory, "Season " + str(season))

        if not update:
            os.makedirs(directory)
            if not os.path.isdir(directory):
                return {"error_title": "Error creating directory",
                        "error_text": "Was a valid directory string entered?"}
            os.makedirs(os.path.join(directory, ".icons"))

        season_update = False
        if update and os.path.isdir(target_directory):
            season_update = True

        if not season_update:
            os.makedirs(target_directory)

        episodes = os.listdir(target_directory)
        first_episode = len(episodes) + 1

        if main_icon:
            if BatchDownloadManager.get_icon(main_icon, os.path.join(directory, ".icons"), "main.png")\
                    == "error":
                return {"error_title": "Error retrieving image from source", "error_text": ""}
        if secondary_icon:
            if BatchDownloadManager.get_icon(secondary_icon, os.path.join(directory, ".icons"),
                                             os.path.dirname(target_directory) + ".png") == "error":
                return {"error_title": "Error retrieving image from source", "error_text": ""}

        if main_icon or secondary_icon:
            DeepIconizer(directory, iconizer_method).iconize()

        if first_episode_string:
            try:
                first_episode = int(first_episode_string)
            except ValueError:
                return {"error_title": "Not a valid episode number", "error_text": ""}

        return {"directory": directory, "show": show, "season": season, "first_episode": first_episode,
                "special": special, "target_directory": target_directory}

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
        # Get the downloader implementation selected by the user
        downloader_implementation = DownloaderManager.get_downloader_from_string(downloader)

        # User different arguments depending on if auto-renaming is desired
        if auto_rename and not preparation["special"]:
            # Use the full constructor
            # noinspection PyCallingNonCallable
            downloader_implementation(packs,
                                      progress_struct,
                                      preparation["target_directory"],
                                      preparation["show"],
                                      preparation["first_episode"],
                                      preparation["season"]).download_loop()
        else:
            # only use the necessary constructor arguments
            # noinspection PyCallingNonCallable
            downloader_implementation(packs, progress_struct, preparation["target_directory"]).download_loop()

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
            second_icon = os.path.join(directory, ".icons", "Season " + str(highest_season) + ".png")

        return show_name, str(highest_season), str(episode_amount), main_icon, second_icon
