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
    from media_manager.plugins.batchdownloadmanager.searchengines.IntelGetter import IntelGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.IxIRCGetter import IxIRCGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.NIBLGetter import NIBLGetter
    from media_manager.plugins.batchdownloadmanager.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
    from media_manager.guitemplates.gtk.GenericGtkGui import GenericGtkGui
    from media_manager.plugins.batchdownloadmanager.downloaders.TwistedDownloader import TwistedDownloader
    from media_manager.plugins.common.fileops.FileMover import FileMover
    from media_manager.plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from media_manager.plugins.batchdownloadmanager.utils.BatchDownloadManager import BatchDownloadManager
except ImportError:
    from plugins.batchdownloadmanager.searchengines.IntelGetter import IntelGetter
    from plugins.batchdownloadmanager.searchengines.IxIRCGetter import IxIRCGetter
    from plugins.batchdownloadmanager.searchengines.NIBLGetter import NIBLGetter
    from plugins.batchdownloadmanager.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
    from guitemplates.gtk.GenericGtkGui import GenericGtkGui
    from plugins.batchdownloadmanager.downloaders.TwistedDownloader import TwistedDownloader
    from plugins.common.fileops.FileMover import FileMover
    from plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from plugins.batchdownloadmanager.utils.BatchDownloadManager import BatchDownloadManager


class BatchDownloadManagerGUI(GenericGtkGui, BatchDownloadManager):
    """
    GUI for the BatchDownloadManager plugin
    """
    
    def __init__(self, parent):
        """
        Constructor
        :param parent: the parent gui
        :return: void
        """
        self.search_result = []
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
        self.directory_content = None
        self.divider_1 = None
        self.divider_2 = None
        super().__init__("Batch Download Manager", parent, True)
        self.grid.set_column_homogeneous(False)
        self.grid.set_row_homogeneous(False)

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return: void
        """

        self.destination_label = self.generate_label("Destination Directory")
        self.destination = self.generate_text_entry("")
        self.destination.connect("changed", self.on_directory_changed)
        self.destination_browser = self.generate_simple_button("Browse", self.browse_for_destination)
        self.grid.attach(self.destination_label, 0, 0, 10, 5)
        self.grid.attach(self.destination_browser, 10, 0, 10, 5)
        self.grid.attach(self.destination, 20, 0, 20, 5)

        self.show_label = self.generate_label("Show Name")
        self.show = self.generate_text_entry("")
        self.grid.attach(self.show_label, 0, 5, 20, 5)
        self.grid.attach(self.show, 20, 5, 20, 5)

        self.season_label = self.generate_label("Season Number")
        self.season = self.generate_text_entry("")
        self.grid.attach(self.season_label, 0, 10, 20, 5)
        self.grid.attach(self.season, 20, 10, 20, 5)

        self.episode_label = self.generate_label("Starting Episode Number")
        self.episode = self.generate_text_entry("optional")
        self.grid.attach(self.episode_label, 0, 15, 20, 5)
        self.grid.attach(self.episode, 20, 15, 20, 5)

        self.search_label = self.generate_label("Search Term")
        self.search_field = self.generate_text_entry("", self.search_xdcc)
        self.grid.attach(self.search_label, 0, 25, 20, 5)
        self.grid.attach(self.search_field, 20, 25, 20, 5)

        self.search_engine_label = self.generate_label("Search Engine")
        self.search_engine_combo_box = self.generate_combo_box(["NIBL.co.uk", "ixIRC.com", "intel.haruhichan.com"])
        self.grid.attach(self.search_engine_label, 0, 30, 20, 5)
        self.grid.attach(self.search_engine_combo_box["combo_box"], 20, 30, 20, 5)

        self.search_button = self.generate_simple_button("Start Search", self.search_xdcc)
        self.grid.attach(self.search_button, 0, 40, 40, 5)

        self.download_engine_label = self.generate_label("Download Engine")
        self.download_engine_combo_box = self.generate_combo_box(["Hexchat Plugin", "Twisted"])
        self.grid.attach(self.download_engine_label, 0, 50, 20, 5)
        self.grid.attach(self.download_engine_combo_box["combo_box"], 20, 50, 20, 5)

        self.options_label = self.generate_label("Options")
        self.rename_check = self.generate_check_box("Automatic Rename", True)
        self.grid.attach(self.options_label, 0, 60, 20, 5)
        self.grid.attach(self.rename_check, 20, 60, 20, 5)

        self.main_icon_label = self.generate_label("Main Icon")
        self.secondary_icon_label = self.generate_label("Season Icon")
        self.main_icon_location = self.generate_text_entry("")
        self.secondary_icon_location = self.generate_text_entry("")
        self.method_label = self.generate_label("Method")
        self.method_combo_box = self.generate_combo_box(["Nautilus", "Nemo"])
        self.grid.attach(self.main_icon_label, 0, 70, 20, 5)
        self.grid.attach(self.secondary_icon_label, 0, 75, 20, 5)
        self.grid.attach(self.main_icon_location, 20, 70, 20, 5)
        self.grid.attach(self.secondary_icon_location, 20, 75, 20, 5)
        self.grid.attach(self.method_label, 0, 80, 20, 5)
        self.grid.attach(self.method_combo_box["combo_box"], 20, 80, 20, 5)

        self.download_button = self.generate_simple_button("Start Download", self.start_download)
        self.grid.attach(self.download_button, 0, 90, 40, 5)

        self.search_results = self.generate_multi_list_box(
            {"types": [int, str, int, str, str], "titles": ["#", "Bot", "Pack", "Size", "Filename"]})
        self.grid.attach(self.search_results["scrollable"], 45, 0, 60, 100)

        self.directory_content = self.generate_multi_list_box({"types": [str], "titles": ["File Name"]})
        self.grid.attach(self.directory_content["scrollable"], 110, 0, 20, 100)

    def search_xdcc(self, widget):
        """
        Searches for xdcc packs using the currently selected search engine
        :param widget: the search button
        :return: void
        """
        if widget is not None:
            search_engine = self.get_current_selected_combo_box_option(self.search_engine_combo_box)
            search_term = self.search_field.get_text()
            self.search_result = self.conduct_xdcc_search(search_engine, search_term)

            list_store = self.search_results["list_store"]
            list_store.clear()
            i = 0
            for result in self.search_result:
                choice = (i,) + result.to_tuple()
                list_store.append(list(choice))
                i += 1

    def start_download(self, widget):
        """
        Starts the Download
        :param widget: the Download Button
        :return: void
        """
        if widget is None:
            return

        preparation = self.prepare(self.destination.get_text(),
                                   self.show.get_text(),
                                   self.season.get_text(),
                                   self.episode.get_text(),
                                   self.main_icon_location.get_text(),
                                   self.secondary_icon_location.get_text(),
                                   self.get_current_selected_combo_box_option(self.method_combo_box))
        if len(preparation) != 6:
            self.show_message_dialog(preparation[0], preparation[1])
            return

        directory, show, season, first_episode, special, new_directory = preparation

        selected_packs = self.get_selected_multi_list_box_elements(self.search_results)
        packs = []
        for selection in selected_packs:
            packs.append(self.search_result[selection])
        if len(packs) == 0:
            return

        downloader = self.get_current_selected_combo_box_option(self.download_engine_combo_box)
        files = []
        if downloader == "Hexchat Plugin":
            if self.rename_check.get_active() and not special:
                files = HexChatPluginDownloader(packs, show, first_episode, season).download_loop()
            else:
                files = HexChatPluginDownloader(packs).download_loop()
        elif downloader == "Twisted":
            if self.rename_check.get_active() and not special:
                files = TwistedDownloader(packs, show, first_episode, season).download_loop()
            else:
                files = TwistedDownloader(packs).download_loop()

        for file in files:
            FileMover.move_file(file, new_directory)

    def on_directory_changed(self, widget):
        """
        method run when the directory changes
        :param widget: the changed widget
        :return: void
        """
        if widget is None:
            return
        directory = self.destination.get_text()
        try:
            show_name = directory.rsplit("/", 1)[1]
        except IndexError:
            show_name = directory.rsplit("/", 1)[0]
        self.show.set_text(show_name)
        self.search_field.set_text(show_name + " 1080")

        self.directory_content["list_store"].clear()
        if os.path.isdir(directory):
            highest_season = 1
            while os.path.isdir(directory + "/Season" + str(highest_season + 1)):
                highest_season += 1
            if os.path.isdir(directory + "/Season " + str(highest_season)):
                children = os.listdir(directory + "/Season " + str(highest_season))
                for child in children:
                    self.directory_content["list_store"].append([child])
                self.episode.set_text(str(len(children) + 1))
                self.season.set_text(str(highest_season))
                main_icon = directory + "/.icons/media_manager.png"
                if os.path.isfile(main_icon):
                    self.main_icon_location.set_text(main_icon)
                secondary_icon = directory + "/.icons/Season " + str(highest_season) + ".png"
                if os.path.isfile(secondary_icon):
                    self.secondary_icon_location.set_text(secondary_icon)

    def browse_for_destination(self, widget):
        """
        Opens a file browser dialog to select a directory to the show's root directory
        :param widget: the button that caused this method call
        :return: void
        """
        if widget is not None:
            directory = self.show_directory_chooser_dialog()
            self.destination.set_text(directory)