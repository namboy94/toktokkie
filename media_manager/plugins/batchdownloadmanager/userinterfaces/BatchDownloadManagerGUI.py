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
import time
from threading import Thread

try:
    from plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from plugins.batchdownloadmanager.utils.BatchDownloadManager import BatchDownloadManager
    from plugins.batchdownloadmanager.utils.ProgressStruct import ProgressStruct
    from Globals import Globals
except ImportError:
    from media_manager.plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from media_manager.plugins.batchdownloadmanager.utils.BatchDownloadManager import BatchDownloadManager
    from media_manager.plugins.batchdownloadmanager.utils.ProgressStruct import ProgressStruct
    from media_manager.Globals import Globals


class BatchDownloadManagerGUI(Globals.selected_grid_gui_framework, BatchDownloadManager):
    """
    GUI for the BatchDownloadManager plugin
    """

    def __init__(self, parent):
        """
        Constructor
        :param parent: the parent gui
        :return: void
        """
        # Threads
        self.search_thread = None
        self.searching = False
        self.dl_progress = None

        # GUI Elements
        self.search_result = []
        self.configure_label = None
        self.destination_label = None
        self.destination = None
        self.destination_browser = None
        self.show_label = None
        self.show = None
        self.season_label = None
        self.season = None
        self.episode_label = None
        self.episode = None
        self.search_label = None
        self.search_field = None
        self.search_engine_label = None
        self.search_engine_combo_box = None
        self.search_button = None
        self.download_engine_label = None
        self.download_engine_combo_box = None
        self.download_button = None
        self.options_label = None
        self.rename_check = None
        self.main_icon_label = None
        self.main_icon_location = None
        self.secondary_icon_label = None
        self.secondary_icon_location = None
        self.method_label = None
        self.method_combo_box = None
        self.search_results = None
        self.search_results_label = None
        self.directory_content = None
        self.directory_content_label = None
        self.total_progress_bar = None
        self.total_progress_label = None
        self.single_progress_bar = None
        self.single_progress_label = None
        self.download_speed = None
        self.download_speed_label = None

        # Initialization
        super().__init__("Batch Download Manager", parent, True)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return: void
        """

        self.configure_label = self.generate_label("Options")
        self.position_absolute(self.configure_label, 0, 0, 40, 5)

        self.destination_label = self.generate_label("Destination Directory")
        self.destination = self.generate_text_entry("", on_changed_command=self.on_directory_changed)
        self.destination_browser = self.generate_button("Browse", self.browse_for_destination)
        self.position_absolute(self.destination_label, 0, 5, 8, 5)
        self.position_absolute(self.destination_browser, 10, 5, 8, 5)
        self.position_absolute(self.destination, 20, 5, 20, 5)

        self.show_label = self.generate_label("Show Name")
        self.show = self.generate_text_entry("")
        self.position_absolute(self.show_label, 0, 10, 20, 5)
        self.position_absolute(self.show, 20, 10, 20, 5)

        self.season_label = self.generate_label("Season Number")
        self.season = self.generate_text_entry("")
        self.position_absolute(self.season_label, 0, 15, 20, 5)
        self.position_absolute(self.season, 20, 15, 20, 5)

        self.episode_label = self.generate_label("Starting Episode Number")
        self.episode = self.generate_text_entry("optional")
        self.position_absolute(self.episode_label, 0, 20, 20, 5)
        self.position_absolute(self.episode, 20, 20, 20, 5)

        self.search_label = self.generate_label("Search Term")
        self.search_field = self.generate_text_entry("", self.search_xdcc)
        self.position_absolute(self.search_label, 0, 30, 20, 5)
        self.position_absolute(self.search_field, 20, 30, 20, 5)

        self.search_engine_label = self.generate_label("Search Engine")
        self.search_engine_combo_box = self.generate_string_combo_box(
            ["NIBL.co.uk", "ixIRC.com", "intel.haruhichan.com"])
        self.position_absolute(self.search_engine_label, 0, 35, 20, 5)
        self.position_absolute(self.search_engine_combo_box, 20, 35, 20, 5)

        self.search_button = self.generate_button("Start Search", self.search_xdcc)
        self.position_absolute(self.search_button, 0, 45, 40, 5)

        self.download_engine_label = self.generate_label("Download Engine")
        self.download_engine_combo_box = self.generate_string_combo_box(["Twisted", "Hexchat Plugin"])
        self.position_absolute(self.download_engine_label, 0, 55, 20, 5)
        self.position_absolute(self.download_engine_combo_box, 20, 55, 20, 5)

        self.options_label = self.generate_label("Options")
        self.rename_check = self.generate_check_box("Automatic Rename", True)
        self.position_absolute(self.options_label, 0, 65, 20, 5)
        self.position_absolute(self.rename_check, 20, 65, 20, 5)

        self.main_icon_label = self.generate_label("Main Icon")
        self.secondary_icon_label = self.generate_label("Season Icon")
        self.main_icon_location = self.generate_text_entry("")
        self.secondary_icon_location = self.generate_text_entry("")
        self.method_label = self.generate_label("Method")
        self.method_combo_box = self.generate_string_combo_box(DeepIconizer.get_iconizer_options())
        self.position_absolute(self.main_icon_label, 0, 75, 20, 5)
        self.position_absolute(self.secondary_icon_label, 0, 80, 20, 5)
        self.position_absolute(self.main_icon_location, 20, 75, 20, 5)
        self.position_absolute(self.secondary_icon_location, 20, 80, 20, 5)
        self.position_absolute(self.method_label, 0, 85, 20, 5)
        self.position_absolute(self.method_combo_box, 20, 85, 20, 5)

        self.download_button = self.generate_button("Start Download", self.start_download)
        self.position_absolute(self.download_button, 0, 95, 40, 5)

        self.total_progress_bar = self.generate_percentage_progress_bar()
        self.total_progress_label = self.generate_label("Total Progress")
        self.single_progress_bar = self.generate_percentage_progress_bar()
        self.single_progress_label = self.generate_label("Single Progress")
        self.download_speed = self.generate_label("-")
        self.download_speed_label = self.generate_label("Download Speed")
        self.position_absolute(self.total_progress_bar, 20, 105, 20, 5)
        self.position_absolute(self.total_progress_label, 0, 105, 20, 5)
        self.position_absolute(self.single_progress_bar, 20, 115, 20, 5)
        self.position_absolute(self.single_progress_label, 0, 115, 20, 5)
        self.position_absolute(self.download_speed, 20, 125, 20, 5)
        self.position_absolute(self.download_speed_label, 0, 125, 20, 5)

        self.search_results_label = self.generate_label("Search Results")
        self.directory_content_label = self.generate_label("Episodes")
        self.position_absolute(self.search_results_label, 50, 0, 60, 5)
        self.position_absolute(self.directory_content_label, 120, 0, 20, 5)

        self.search_results = self.generate_primitive_multi_list_box(
            {"#": (0, int), "Bot": (1, str), "Pack": (2, int), "Size": (3, str), "Filename": (4, str)})
        self.position_absolute(self.search_results, 50, 5, 60, 95)

        self.directory_content = self.generate_primitive_multi_list_box({"File Name": (0, str)})
        self.position_absolute(self.directory_content, 120, 5, 20, 95)

    def search_xdcc(self, widget):
        """
        Searches for xdcc packs using the currently selected search engine, using a seperate thread
        If a search is already running, it won't start a new search
        :param widget: the search button
        :return: void
        """
        def search_xdcc_thread():
            """
            To be run as an individual thread so that the GUI doesn't freeze while searching
            """
            self.searching = True

            self.set_button_string(self.search_button, "Searching...")
            search_engine = self.get_string_from_current_selected_combo_box_option(self.search_engine_combo_box)
            search_term = self.get_string_from_text_entry(self.search_field)
            self.search_result = self.conduct_xdcc_search(search_engine, search_term)

            self.clear_primitive_multi_list_box(self.search_results)
            i = 0
            for result in self.search_result:
                choice = (i,) + result.to_tuple()
                self.add_primitive_multi_list_box_element(self.search_results, choice)
                i += 1
            self.search_button.set_label("Start Search")
            self.searching = False
            self.search_thread = None

        if widget is not None and not self.searching and self.search_thread is None:
                self.search_thread = self.run_sensitive_thread_in_parallel(search_xdcc_thread)

    def start_download(self, widget):
        """
        Starts the Download
        :param widget: the Download Button
        :return: void
        """

        if widget is None or self.dl_progress is not None:
            return

        def update_progress_thread(progress_struct):
            """
            Updates the progress UI elements
            :param progress_struct: the progress structure to be displayed
            :return: void
            """
            while True:
                total_progress = float(progress_struct.total_progress) / float(progress_struct.total)
                self.total_progress_bar.set_fraction(total_progress)
                single_progress = float(progress_struct.single_progress) / float(progress_struct.single_size)
                self.single_progress_bar.set_fraction(single_progress)
                if progress_struct.total == progress_struct.total_progress:
                    self.download_button.set_label("Download")
                    self.dl_progress = None
                    break
                time.sleep(1)

        preparation = self.prepare(self.get_string_from_text_entry(self.destination),
                                   self.get_string_from_text_entry(self.show),
                                   self.get_string_from_text_entry(self.season),
                                   self.get_string_from_text_entry(self.episode),
                                   self.get_string_from_text_entry(self.main_icon_location),
                                   self.get_string_from_text_entry(self.secondary_icon_location),
                                   self.get_string_from_current_selected_combo_box_option(self.method_combo_box))

        if len(preparation) != 6:
            self.show_message_dialog(preparation[0], preparation[1])
            return

        selected_packs = self.get_list_of_selected_elements_from_multi_list_box(self.search_results)
        packs = []
        for selection in selected_packs:
            packs.append(self.search_result[selection[0]])
        if len(packs) == 0:
            return

        self.set_button_string("Downloading...")

        downloader = self.get_string_from_current_selected_combo_box_option(self.download_engine_combo_box)
        progress = ProgressStruct()
        progress.total = len(packs)

        self.run_thread_in_parallel(target=update_progress_thread, args=(progress,))

        self.run_thread_in_parallel(target=self.start_download_process,
                                    args=(preparation, downloader, packs, self.rename_check.get_active(), progress))
        self.dl_progress = progress

    def on_directory_changed(self, widget):
        """
        method run when the directory changes
        :param widget: the changed widget
        :return: void
        """
        if widget is None:
            return
        directory = self.get_string_from_text_entry(self.destination)
        show_name = os.path.basename(directory)
        self.set_text_entry_string(self.show, show_name)
        self.set_text_entry_string(self.search_field, show_name)

        self.clear_primitive_multi_list_box(self.directory_content)
        if os.path.isdir(directory):
            highest_season = 1
            while os.path.isdir(os.path.join(directory, "Season " + str(highest_season + 1))):
                highest_season += 1
            if os.path.isdir(os.path.join(directory, "Season " + str(highest_season))):
                children = os.listdir(os.path.join(directory, "Season " + str(highest_season)))
                for child in children:
                    self.add_primitive_multi_list_box_element(child)
                self.set_text_entry_string(self.episode, str(len(children) + 1))
                self.set_text_entry_string(self.season, str(highest_season))
                main_icon = os.path.join(directory, ".icons", "main.png")
                if os.path.isfile(main_icon):
                    self.set_text_entry_string(self.main_icon_location, main_icon)
                secondary_icon = os.path.join(directory, ".icons", "Season " + str(highest_season) + ".png")
                if os.path.isfile(secondary_icon):
                    self.set_text_entry_string(self.secondary_icon_location, secondary_icon)

    def browse_for_destination(self, widget):
        """
        Opens a file browser dialog to select a directory to the show's root directory
        :param widget: the button that caused this method call
        :return: void
        """
        if widget is not None:
            directory = self.show_directory_chooser_dialog()
            self.set_text_entry_string(self.destination, directory)
