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

    def start(self, title=None):
        """
        Starts the main program loop
        :return: void
        """
        super().start("BATCH DOWNLOAD MANAGER PLUGIN\n")

    def mainloop(self, directory=None, use_defaults=None, show_name_override=None,
                 season_number_override=None, first_episode_override=None,
                 search_engine=None, search_term=None, auto_rename=None):
        """
        The main program loop
        :return: void
        """
        self.restore_start_state()

        self.directory = directory
        if self.directory is None:
            self.directory = self.ask_user("Enter the target download directory:")
        if not self.directory:
            print("Invalid directory")
            return

        show_name, season, starting_episode_number = self.check_show_directory(self.directory)

        if directory is None:

            self.show_name = self.ask_user("Please enter the show name:", default=show_name)
            if os.path.basename(self.directory) != self.show_name:
                print("Are you sure that " + self.show_name + " is correct? (y/n)")
                response = self.ask_user()
                if response != "y":
                    return

            while self.season == "":
                try:
                    self.season = int(self.ask_user("Please enter the season number:", default=season))
                except ValueError:
                    "Invalid integer value.\n"

            while self.starting_episode_number == "":
                try:
                    self.starting_episode_number = int(self.ask_user("Please enter the first episode number:",
                                                                     default=starting_episode_number))
                except ValueError:
                    "Invalid integer value.\n"
            self.search_xdcc()

        else:
            if use_defaults is not None:
                self.show_name = show_name
                self.season = season
                self.starting_episode_number = starting_episode_number
            if show_name_override is not None:
                self.show_name = show_name_override
            if season_number_override is not None:
                self.season = season_number_override
            if first_episode_override is not None:
                self.starting_episode_number = first_episode_override
            if search_term is None:
                search_term = self.show_name

            self.search_xdcc(search_engine, search_term)

        if auto_rename is None:

            auto_rename_prompt = self.ask_user("Auto Rename? (y/n)")
            if auto_rename_prompt == "y":
                self.auto_rename = True

        else:

            if auto_rename:
                self.auto_rename = True
            else:
                self.auto_rename = False

        self.start_download()

    def search_xdcc(self, search_engine_override=None, search_term_override=None):
        """
        Searches for xdcc packs
        :return: void
        """
        searching = True
        print("Starting Search Procedure:")
        while searching:
            if search_engine_override is not None:
                search_engine_selected = True
                self.search_engine = search_engine_override
            else:
                search_engine_selected = False
            while not search_engine_selected:
                print("Search Engine Options:\n")
                print("1: NIBL.co.uk")
                print("2: ixIRC.com")
                print("3: intel.haruhichan.com")
                try:
                    search_engine = int(self.ask_user("Which search engine would you like to use?", default="1"))
                    if search_engine == 1:
                        self.search_engine = "NIBL.co.uk"
                    elif search_engine == 2:
                        self.search_engine = "ixIRC.com"
                    elif search_engine == 3:
                        self.search_engine = "intel.haruhichan.com"
                    else:
                        print("Invalid index")
                        continue
                    search_engine_selected = True
                except ValueError:
                    print("Not a valid integer")

            search_term = search_term_override
            if search_term_override is None:
                search_term = self.ask_user("Search for what?", default=self.show_name)

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

                selection = self.ask_user("Enter a comma-delimited selection of packs to download, "
                                          "or blank to conduct a new search:\n")

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
                    if search_term_override is None:
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

    @staticmethod
    def check_show_directory(directory):
        """
        method that calculates the default values for a show directory
        :param directory: the directory to be checked
        :return: the show name, the highest season, the amount of episodes
        """
        show_name = os.path.basename(directory)
        highest_season = 0
        episode_amount = 0

        if os.path.isdir(directory):
            highest_season = 1
            while os.path.isdir(os.path.join(directory, "Season " + str(highest_season + 1))):
                highest_season += 1
            if os.path.isdir(os.path.join(directory, "Season " + str(highest_season))):
                children = os.listdir(os.path.join(directory, "Season " + str(highest_season)))
                episode_amount = len(children) + 1

        return show_name, str(highest_season), str(episode_amount)

    def restore_start_state(self):
        """
        Restores the state of the BatchDownloadManagerCli object to what it was at the beginning.
        :return: void
        """
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
