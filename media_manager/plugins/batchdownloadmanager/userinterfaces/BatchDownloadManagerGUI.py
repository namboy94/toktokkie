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


class BatchDownloadManagerGUI(Globals.selected_grid_gui_framework):
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
        self.total_progress_current = None
        self.total_progress_total = None
        self.single_progress_bar = None
        self.single_progress_label = None
        self.single_progress_current = None
        self.single_progress_total = None
        self.download_speed = None
        self.download_speed_label = None
        self.average_dl_speed = None
        self.average_dl_speed_label = None
        self.time_left = None
        self.time_left_label = None

        # Initialization
        super().__init__("Batch Download Manager", parent, True)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return: void
        """

        # Show Information
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

        # Icon Information
        self.main_icon_label = self.generate_label("Main Icon")
        self.secondary_icon_label = self.generate_label("Season Icon")
        self.main_icon_location = self.generate_text_entry("")
        self.secondary_icon_location = self.generate_text_entry("")
        self.method_label = self.generate_label("Method")
        self.method_combo_box = self.generate_string_combo_box(DeepIconizer.get_iconizer_options())
        self.position_absolute(self.main_icon_label, 0, 55, 20, 5)
        self.position_absolute(self.secondary_icon_label, 0, 60, 20, 5)
        self.position_absolute(self.main_icon_location, 20, 55, 20, 5)
        self.position_absolute(self.secondary_icon_location, 20, 60, 20, 5)
        self.position_absolute(self.method_label, 0, 65, 20, 5)
        self.position_absolute(self.method_combo_box, 20, 65, 20, 5)

        # Multi List Boxes
        self.search_results_label = self.generate_label("Search Results")
        self.directory_content_label = self.generate_label("Episodes")
        self.position_absolute(self.search_results_label, 50, 0, 60, 5)
        self.position_absolute(self.directory_content_label, 120, 0, 20, 5)

        self.search_results = self.generate_primitive_multi_column_list_box(
            {"#": (0, int), "Bot": (1, str), "Pack": (2, int), "Size": (3, str), "Filename": (4, str)})
        self.position_absolute(self.search_results, 50, 5, 70, 40)

        self.directory_content = self.generate_primitive_multi_column_list_box({"File Name": (0, str)})
        self.position_absolute(self.directory_content, 120, 5, 30, 40)

        # Download Section
        self.options_label = self.generate_label("Automatic Rename")
        self.rename_check = self.generate_check_box("", True)
        self.position_absolute(self.options_label, 80, 45, 15, 12)
        self.position_absolute(self.rename_check, 95, 45, 15, 12)

        self.download_engine_label = self.generate_label("Download Engine")
        self.download_engine_combo_box = self.generate_string_combo_box(["Twisted", "Hexchat Plugin"])
        self.position_absolute(self.download_engine_label, 80, 57, 15, 13)
        self.position_absolute(self.download_engine_combo_box, 95, 57, 15, 13)

        self.download_button = self.generate_button("Start Download", self.start_download)
        self.position_absolute(self.download_button, 50, 45, 30, 25)

        self.total_progress_bar = self.generate_percentage_progress_bar()
        self.total_progress_label = self.generate_label("Total Progress")
        self.total_progress_current = self.generate_label("")
        self.total_progress_total = self.generate_label("")
        self.single_progress_bar = self.generate_percentage_progress_bar()
        self.single_progress_label = self.generate_label("Single Progress")
        self.single_progress_current = self.generate_label("")
        self.single_progress_total = self.generate_label("")
        self.download_speed = self.generate_label("-")
        self.download_speed_label = self.generate_label("Download Speed")
        self.average_dl_speed = self.generate_label("-")
        self.average_dl_speed_label = self.generate_label("Average Speed")
        self.time_left = self.generate_label("-")
        self.time_left_label = self.generate_label("Time Left")
        self.position_absolute(self.total_progress_bar, 128, 45, 19, 5)
        self.position_absolute(self.total_progress_label, 110, 45, 15, 5)
        self.position_absolute(self.total_progress_current, 125, 45, 3, 5)
        self.position_absolute(self.total_progress_total, 147, 45, 3, 5)
        self.position_absolute(self.single_progress_bar, 128, 50, 19, 5)
        self.position_absolute(self.single_progress_label, 110, 50, 15, 5)
        self.position_absolute(self.single_progress_current, 125, 50, 3, 5)
        self.position_absolute(self.single_progress_total, 147, 50, 3, 5)
        self.position_absolute(self.download_speed, 128, 55, 19, 5)
        self.position_absolute(self.download_speed_label, 110, 55, 15, 5)
        self.position_absolute(self.average_dl_speed, 128, 60, 19, 5)
        self.position_absolute(self.average_dl_speed_label, 110, 60, 15, 5)
        self.position_absolute(self.time_left, 128, 65, 19, 5)
        self.position_absolute(self.time_left_label, 110, 65, 15, 5)

    def search_xdcc(self, widget):
        """
        Searches for xdcc packs using the currently selected search engine, using a seperate thread
        If a search is already running, it won't start a new search
        :param widget: the search button
        :return: void
        """
        if widget is None or self.searching or self.search_thread is not None:
            return

        def search():
            """
            Searches using the speciifed search engine
            """
            self.searching = True
            self.run_thread_safe(self.set_button_string, (self.search_button, "Searching..."))

            search_engine = self.get_string_from_current_selected_combo_box_option(self.search_engine_combo_box)
            search_term = self.get_string_from_text_entry(self.search_field)
            self.search_result = BatchDownloadManager.conduct_xdcc_search(search_engine, search_term)

        def search_xdcc_thread():
            """
            To be run as an individual thread so that the GUI doesn't freeze while searching
            """
            self.clear_primitive_multi_list_box(self.search_results)
            i = 0
            for result in self.search_result:
                choice = (i,) + result.to_tuple()
                self.add_primitive_multi_list_box_element(self.search_results, choice)
                i += 1
            self.run_thread_safe(self.set_button_string, (self.search_button, "Start Search"))
            self.searching = False
            self.search_thread = None

        self.search_thread = self.run_sensitive_thread_in_parallel(target=search_xdcc_thread, insensitive_target=search)

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
            def complete_dl():
                """
                Run when the download has completed
                """
                self.set_button_string(self.download_button, "Download")
                self.reset_percentage_progress_bar(self.single_progress_bar)
                self.reset_percentage_progress_bar(self.total_progress_bar)
                self.set_label_string(self.download_speed, "-")
                self.clear_label_text(self.total_progress_current)
                self.clear_label_text(self.total_progress_total)
                self.clear_label_text(self.single_progress_current)
                self.clear_label_text(self.single_progress_total)
                self.on_directory_changed(1)

            def update():
                """
                Updates the widgets with new values
                """
                # calculate
                try:
                    single_progress = float(progress_struct.single_progress) / float(progress_struct.single_size)
                except ZeroDivisionError:
                    single_progress = 0.0
                total_progress = float(progress_struct.total_progress) / float(progress_struct.total)
                total_progress_percentage = total_progress + (single_progress / progress_struct.total)

                # update
                self.set_progress_bar_float_percentage(self.total_progress_bar, total_progress_percentage)
                self.set_progress_bar_float_percentage(self.single_progress_bar, single_progress)
                self.set_label_string(self.total_progress_current, str(progress_struct.total_progress))
                self.set_label_string(self.total_progress_total, str(progress_struct.total))
                self.set_label_string(self.single_progress_current, str(progress_struct.single_progress))
                self.set_label_string(self.single_progress_total, str(progress_struct.single_size))

            last_single_progress_size = 0.0
            speed_time_counter = 0
            total_time_counter = 0

            while True:

                self.run_thread_safe(update)

                if float(progress_struct.single_progress) != last_single_progress_size:
                    speed = (float(progress_struct.single_progress) - last_single_progress_size) / speed_time_counter
                    speed_time_counter = 0
                    last_single_progress_size = float(progress_struct.single_progress)

                    average_speed = int(float(progress_struct.single_progress) / total_time_counter)
                    time_left = int(progress_struct.single_size / average_speed)

                    self.run_thread_safe(self.set_label_string, (self.download_speed, str(int(speed)) + " Byte/s"))
                    self.run_thread_safe(self.set_label_string, (self.average_dl_speed, str(average_speed) + " Byte/s"))
                    self.run_thread_safe(self.set_label_string, (self.time_left, str(time_left) + "s"))

                if progress_struct.total == progress_struct.total_progress:
                    self.run_thread_safe(complete_dl)
                    self.dl_progress = None
                    break
                speed_time_counter += 1
                total_time_counter += 1
                time.sleep(1)

        preparation = BatchDownloadManager.prepare(self.get_string_from_text_entry(self.destination),
                                                   self.get_string_from_text_entry(self.show),
                                                   self.get_string_from_text_entry(self.season),
                                                   self.get_string_from_text_entry(self.episode),
                                                   self.get_string_from_text_entry(self.main_icon_location),
                                                   self.get_string_from_text_entry(self.secondary_icon_location),
                                                   self.get_string_from_current_selected_combo_box_option(
                                                       self.method_combo_box))

        if len(preparation) != 6:
            self.show_message_dialog(preparation[0], preparation[1])
            return

        selected_packs = self.get_list_of_selected_elements_from_multi_list_box(self.search_results)
        packs = []
        for selection in selected_packs:
            packs.append(self.search_result[selection[0]])
        if len(packs) == 0:
            return

        self.set_button_string(self.download_button, "Downloading...")

        downloader = self.get_string_from_current_selected_combo_box_option(self.download_engine_combo_box)
        progress = ProgressStruct()
        progress.total = len(packs)

        self.run_thread_in_parallel(target=update_progress_thread, args=(progress,))

        self.run_thread_in_parallel(target=BatchDownloadManager.start_download_process,
                                    args=(preparation, downloader, packs,
                                          self.get_boolean_from_check_box(self.rename_check), progress))
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
                    self.add_primitive_multi_list_box_element(self.directory_content, (child,))
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
