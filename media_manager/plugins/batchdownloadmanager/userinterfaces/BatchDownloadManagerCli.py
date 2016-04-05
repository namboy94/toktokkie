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
    from plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from plugins.batchdownloadmanager.utils.BatchDownloadManager import BatchDownloadManager
    from plugins.batchdownloadmanager.utils.ProgressStruct import ProgressStruct
    from cli.exceptions.ReturnException import ReturnException
    from cli.GenericCli import GenericCli
except ImportError:
    from media_manager.plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from media_manager.plugins.batchdownloadmanager.utils.BatchDownloadManager import BatchDownloadManager
    from media_manager.plugins.batchdownloadmanager.utils.ProgressStruct import ProgressStruct
    from media_manager.cli.exceptions.ReturnException import ReturnException
    from media_manager.cli.GenericCli import GenericCli


class BatchDownloadManagerCli(GenericCli):
    """
    CLI for the BatchDownloadManager plugin
    """

    def __init__(self, parent):
        """
        Constructor
        :param parent: the parent gui
        :return: void
        """
        super().__init__(parent)
        self.directory = ""
        self.show_name = ""
        self.season = ""
        self.starting_episode_number = ""
        self.search_engine = ""
        self.main_icon = ""
        self.secondary_icon = ""
        self.iconizer = ""
        self.selected_packs = []
        self.auto_rename = False

    def start(self):
        """
        Starts the main program loop
        :return: void
        """

        try:
            print("BATCH DOWNLOAD MANAGER PLUGIN\n")

            self.directory = self.ask_user("Enter the target download directory:\n")

            self.show_name = self.ask_user("Please enter the show name:\n")
            if os.path.basename(self.directory) != self.show_name:
                print("Are you sure that " + self.show_name + " is correct? (y/n)")
                response = self.ask_user()
                if response != "y":
                    return

            while self.season == "":
                try:
                    self.season = int(self.ask_user("Please enter the season number:\n"))
                except ValueError:
                    "Invalid integer value.\n"

            while self.starting_episode_number == "":
                try:
                    self.starting_episode_number = int(self.ask_user("Please enter the first episode number:\n"))
                except ValueError:
                    "Invalid integer value.\n"

            self.search_xdcc()

            auto_rename_prompt = self.ask_user("Auto Rename? (y/n)")
            if auto_rename_prompt == "y":
                self.auto_rename = True

            self.start_download()

            self.start()

        except ReturnException:
            self.stop()

    def search_xdcc(self):
        """
        Searches for xdcc packs
        :return: void
        """
        searching = True
        print("Starting Search Procedure:")
        while searching:
            search_engine_selected = False
            while not search_engine_selected:
                print("Search Engine Options:\n")
                print("1: NIBL.co.uk")
                print("2: ixIRC.com")
                print("3: intel.haruhichan.com")
                try:
                    search_engine = int(self.ask_user("Which search engine would you like to use?"))
                    if search_engine == 1:
                        self.search_engine = "NIBL.co.uk"
                    elif search_engine == 2:
                        self.search_engine = "NIBL.co.uk"
                    elif search_engine == 3:
                        self.search_engine = "NIBL.co.uk"
                    else:
                        print("Invalid index")
                        continue
                    search_engine_selected = True
                except ValueError:
                    print("Not a valid integer")

            search_term = self.ask_user("Search for what?\n")
            print("searching...")
            search_result = BatchDownloadManager.conduct_xdcc_search(self.search_engine, search_term)
            print("Results:")
            i = 0
            result_dict = {}
            for result in search_result:
                result_dict[i] = result
                print(str(i) + " " + result.to_string())
                i += 1

            selecting = True
            while selecting:

                selection = \
                    self.ask_user("Enter a comma-delimited selection of packs to download,"
                                  " or blank to conduct a new search:\n")

                if selection == "":
                    break

                selection_list = selection.split(",")
                selected_packs = []

                try:
                    for selected in selection_list:
                        selected_packs.append(result_dict[int(selected)])
                except ValueError:
                    print("Invalid selection type, please only enter the index of the packs you want to select")
                    continue
                except KeyError:
                    print("Invalid index selected")
                    continue

                print("Selection:")
                for pack in selected_packs:
                    print(pack.to_string())
                confirmation = self.ask_user("Do you want to download these packs? (y/n)")
                if confirmation == "y":
                    searching = False
                    selecting = False
                    self.selected_packs = selected_packs
                else:
                    re_search_prompt = self.ask_user("Do you want to re-search? (y/n)")
                    if re_search_prompt == "y":
                        selecting = False

    def start_download(self):
        """
        Starts the Download
        :return: void
        """

        preparation = BatchDownloadManager.prepare(self.directory,
                                                   self.show_name,
                                                   str(self.season),
                                                   str(self.starting_episode_number),
                                                   self.main_icon,
                                                   self.secondary_icon,
                                                   self.iconizer)

        if len(preparation) != 6:
            print(preparation[0])
            print(preparation[1])
            return

        print("Downloading...")

        downloader = "Twisted"
        progress = ProgressStruct()
        progress.total = len(self.selected_packs)

        BatchDownloadManager.start_download_process(
            preparation, downloader, self.selected_packs, self.auto_rename, progress)
