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

# Imports
import os
import random
from subprocess import Popen, PIPE
from typing import List

try:
    from external.__init__ import get_location  # This import is used to find the file location of the twisted script
    from plugins.renamer.objects.Episode import Episode
    from plugins.batchdownloadmanager.utils.ProgressStruct import ProgressStruct
    from plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack
    from plugins.batchdownloadmanager.downloaders.GenericDownloader import GenericDownloader
except ImportError:
    from media_manager.external.__init__ import get_location
    from media_manager.plugins.renamer.objects.Episode import Episode
    from media_manager.plugins.batchdownloadmanager.utils.ProgressStruct import ProgressStruct
    from media_manager.plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack
    from media_manager.plugins.batchdownloadmanager.downloaders.GenericDownloader import GenericDownloader


class TwistedDownloader(GenericDownloader):
    """
    Wrapper for Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes's XDCC Downloader
    The plan is to replace his script with one of my own once twisted supports python 3.

    It can download XDCC packs without the help of any external programs like Hexchat,
    it is currently necessary to have a working python2 environment in which the twisted
    package has been installed
    """

    packs = []
    """
    A list of the packs to download
    """

    progress_struct = None
    """
    A progress structure used to communicate with other threads, for example with a GUI to
    exchange information about the download progress
    """

    target_directory = ""
    """
    The target directory for the downloaded files
    """

    show_name = ""
    """
    The show name (only use when auto-renaming)
    """

    episode_number = -1
    """
    The first episode number (only use when auto-renaming)
    """

    season_number = -1
    """
    The season number (only use when auto-renaming)
    """

    auto_rename = False
    """
    This boolean is True if the program is supposed to automatically rename the downloaded files,
    but otherwise it defaults to False
    """

    # noinspection PyTypeChecker
    def __init__(self, packs: List[XDCCPack], progress_struct: ProgressStruct, target_directory: str,
                 show_name: str = "", episode_number: int = 0, season_number: int = 0) -> None:
        """
        Constructor of the TwistedDownloader class

        It stores given parameter values locally and establishes if it should auto rename or not
        using the GenericDownloader's Constructor.

        This method also checks if the twisted library has implemented IRC/XDCC support for python 3
        and notifies the user in a rather verbose manner when this is the case.

        :param packs: the packs to be downloaded
        :param progress_struct: Structure that keeps track of download progress
        :param target_directory: The target download directory
        :param show_name: the show name for auto renaming
        :param episode_number: the (starting) episode number for auto renaming
        :param season_number: the season number for auto renaming
        :return: None
        """
        # Store variables
        super().__init__(packs, progress_struct, target_directory, show_name, episode_number, season_number)

        # Check for python 3 twisted compatibility
        self.check_python3_compatibility()

    # noinspection PyTypeChecker
    def download_loop(self) -> List[str]:
        """
        Starts the Download loop, which downloads all packs given via parameter in the Constructor

        It also incrementally updates the progress structure's total progress attribute.

        :return: None
        """
        files = []  # The downloaded file paths
        for pack in self.packs:  # Download each pack
            files.append(self.download_single(pack))  # Download pack and append file path to files list
            self.progress_struct.total_progress += 1  # Increment progress structure
        return files

    def download_single(self, pack: XDCCPack) -> str:
        """
        Downloads a single pack with the help of the twisted downloader script
        and also auto-renames the resulting file if auto-rename is enabled

        :param pack: the pack to download
        :return: The file path to the downloaded file
        """
        # Set approximate total size of the single download
        self.progress_struct.single_size = pack.size

        # Print informational string, which file is being downloaded
        print("Downloading pack: " + pack.to_string())

        script = get_location("xdccbot.py")  # Find out location of the xdccbot script
        dl_folder = self.target_directory  # Establish download directory

        # Set up the download command
        dl_command = ["python2",  # The python 2 interpreter
                      script,  # The path to the download script
                      pack.server,  # The server to which the script has to connect
                      pack.channel.split("#", 1)[1],  # The channel to which the script should connect
                      "media_manager_python" + str(random.randint(0, 1000000)),  # The script's username
                      pack.bot,  # The bot to contact for the episode file
                      dl_folder,  # The destination directory of the file
                      str(pack.packnumber)]  # The pack number to download

        proc = Popen(dl_command, stderr=PIPE)  # Starts new process, pipes stderr
        file_name = ""
        while True:  # Reacts on every line written to stderr
            line = proc.stderr.readline().decode().split("\n")[0]

            # New progress, progress structure needs to be updated
            if "PROGRESS:" in line:
                self.progress_struct.single_progress = int(line.split("PROGRESS:")[1])
                single_progress = float(self.progress_struct.single_progress) / float(self.progress_struct.single_size)
                single_progress *= 100.00

                # Format the string to print
                single_progress_formatted_string = "%.2f" % single_progress
                out_string_begin = line.split("INFO:root:")[1] + " / " + str(self.progress_struct.single_size) + " ("

                print(out_string_begin + single_progress_formatted_string + "%)", end="\r")

            # Download has completed, ends the loop
            elif "DLCOMPLETE:" in line:
                file_name = line.split("DLCOMPLETE:")[1]  # Find out file name
                print("Finished Downloading " + file_name)  # Message user that download has completed
                break

        if not file_name:
            raise Exception("Twisted Download Error, File " + pack.filename + " not downloaded")

        file_path = os.path.join(dl_folder, file_name)  # path to file

        # auto rename process:
        if self.auto_rename:
            # Create Episode object
            episode = Episode(file_path, self.episode_number, self.season_number, self.show_name)
            episode.rename()  # Rename file with help of TVDB
            self.episode_number += 1
            return episode.episode_file  # Return the new file path
        else:
            return file_path  # Return the file path

    # noinspection PyUnresolvedReferences
    @staticmethod
    def check_python3_compatibility() -> None:
        """
        Checks if the twisted library has enough support on python 3 to support IRC/XDCC

        If support has been added, a very verbose message is shown to the user to contact the
        developer, so that native support can be added

        :return: None
        """

        # Check if twisted has already implemented the necessary parts of the library
        # for downloading via XDCC for python 3
        try:
            # These packages have to be implemented by twisted
            from twisted.words.protocols import irc

            from twisted.internet import reactor, protocol
            from twisted.python import log as twistedlog
            twisted_irc_implemented_in_python3 = True
        except ImportError:
            twisted_irc_implemented_in_python3 = False

        if twisted_irc_implemented_in_python3:
            # This is supposed to help me get a faster response by annoying users.
            # Has to be stored in a separate variable for python2 compatibility
            twisted_in_python3_warning = "IRC/XDCC HAS BEEN IMPLEMENTED BY THE TWISTED LIBRARY FOR PYTHON 3! "
            twisted_in_python3_warning += "CONTACT THE DEV IMMEDIATELY AT hermann@krumreyh.com or open an issue "
            twisted_in_python3_warning += "at http://gitlab.namibsun.net/media-manager"
            print(twisted_in_python3_warning)

    @staticmethod
    def get_string_identifier() -> str:
        """
        Returns a unique string identifier with which the Downloader can be addressed by
        the DownloaderManager

        :return: the string identifier of the Downloader
        """
        return "Twisted Downloader"
