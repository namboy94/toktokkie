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
from tkinter import END, W, E, N, S, Grid

try:
    from media_manager.plugins.batchdownloadmanager.searchengines.IntelGetter import IntelGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.IxIRCGetter import IxIRCGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.NIBLGetter import NIBLGetter
    from media_manager.plugins.batchdownloadmanager.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
    from media_manager.guitemplates.tk.GenericTkGui import GenericTkGui
    from media_manager.plugins.batchdownloadmanager.downloaders.TwistedDownloader import TwistedDownloader
    from media_manager.plugins.common.fileops.FileMover import FileMover
    from media_manager.plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from media_manager.plugins.batchdownloadmanager.utils.BatchDownloadManager import BatchDownloadManager
except ImportError:
    from plugins.batchdownloadmanager.searchengines.IntelGetter import IntelGetter
    from plugins.batchdownloadmanager.searchengines.IxIRCGetter import IxIRCGetter
    from plugins.batchdownloadmanager.searchengines.NIBLGetter import NIBLGetter
    from plugins.batchdownloadmanager.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
    from guitemplates.tk.GenericTkGui import GenericTkGui
    from plugins.batchdownloadmanager.downloaders.TwistedDownloader import TwistedDownloader
    from plugins.common.fileops.FileMover import FileMover
    from plugins.iconizer.utils.DeepIconizer import DeepIconizer
    from plugins.batchdownloadmanager.utils.BatchDownloadManager import BatchDownloadManager


class BatchDownloadManagerTkGui(GenericTkGui, BatchDownloadManager):
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

    def lay_out(self):
        """
        Sets up all interface elements of the GUI
        :return: void
        """

        self.destination_label = self.generate_label("Destination Directory")
        self.destination = self.generate_text_entry("", change_command=self.on_directory_changed)
        self.destination_browser = self.generate_simple_button("Browse", self.browse_for_destination)
        self.destination_label.grid(columnspan=1, column=0, row=0, sticky=W + E + N + S)
        self.destination.grid(columnspan=2, column=2, row=0, sticky=W + E + N + S)
        self.destination_browser.grid(columnspan=1, column=1, row=0, sticky=W + E + N + S)

        self.show_label = self.generate_label("Show Name")
        self.show = self.generate_text_entry("")
        self.show_label.grid(columnspan=2, column=0, row=1, sticky=W + E + N + S)
        self.show.grid(columnspan=2, column=2, row=1, sticky=W + E + N + S)

        self.season_label = self.generate_label("Season Number")
        self.season = self.generate_text_entry("")
        self.season_label.grid(columnspan=2, column=0, row=2, sticky=W + E + N + S)
        self.season.grid(columnspan=2, column=2, row=2, sticky=W + E + N + S)

        self.episode_label = self.generate_label("Starting Episode Number")
        self.episode = self.generate_text_entry("optional")
        self.episode_label.grid(columnspan=2, column=0, row=3, sticky=W + E + N + S)
        self.episode.grid(columnspan=2, column=2, row=3, sticky=W + E + N + S)

        self.search_label = self.generate_label("Search Term")
        self.search_field = self.generate_text_entry("", self.search_xdcc)
        self.search_label.grid(columnspan=2, column=0, row=4, sticky=W + E + N + S)
        self.search_field.grid(columnspan=2, column=2, row=4, sticky=W + E + N + S)

        self.search_engine_label = self.generate_label("Search Engine")
        self.search_engine_combo_box = self.generate_combo_box(["NIBL.co.uk", "ixIRC.com", "intel.haruhichan.com"])
        self.search_engine_label.grid(columnspan=2, column=0, row=5, sticky=W + E + N + S)
        self.search_engine_combo_box.grid(columnspan=2, column=2, row=5, sticky=W + E + N + S)

        self.search_button = self.generate_simple_button("Start Search", self.search_xdcc)
        self.search_button.grid(columnspan=4, column=0, row=6, sticky=W + E + N + S)

        self.download_engine_label = self.generate_label("Download Engine")
        self.download_engine_combo_box = self.generate_combo_box(["Hexchat Plugin", "Twisted"])
        self.download_engine_label.grid(columnspan=2, column=0, row=7, sticky=W + E + N + S)
        self.download_engine_combo_box.grid(columnspan=2, column=2, row=7, sticky=W + E + N + S)

        self.options_label = self.generate_label("Options")
        self.rename_check = self.generate_check_box("Automatic Rename", True)
        self.options_label.grid(columnspan=2, column=0, row=8, sticky=W + E + N + S)
        self.rename_check.grid(columnspan=2, column=2, row=8, sticky=W + E + N + S)

        self.main_icon_label = self.generate_label("Main Icon")
        self.secondary_icon_label = self.generate_label("Season Icon")
        self.main_icon_location = self.generate_text_entry("")
        self.secondary_icon_location = self.generate_text_entry("")
        self.method_label = self.generate_label("Method")
        self.method_combo_box = self.generate_combo_box([DeepIconizer.get_iconizer_options()])
        self.main_icon_label.grid(columnspan=2, column=0, row=9, sticky=W + E + N + S)
        self.secondary_icon_label.grid(columnspan=2, column=0, row=10, sticky=W + E + N + S)
        self.main_icon_location.grid(columnspan=2, column=2, row=9, sticky=W + E + N + S)
        self.secondary_icon_location.grid(columnspan=2, column=2, row=10, sticky=W + E + N + S)
        self.method_label.grid(columnspan=2, column=0, row=11, sticky=W + E + N + S)
        self.method_combo_box.grid(columnspan=2, column=2, row=11, sticky=W + E + N + S)

        self.download_button = self.generate_simple_button("Start Download", self.start_download)
        self.download_button.grid(columnspan=4, column=0, row=12, sticky=W + E + N + S)

        self.search_results = self.generate_multi_selectable_list_box([])
        self.search_results.grid(columnspan=10, rowspan=12, column=5, row=0, sticky=W + E + N + S)

        self.directory_content = self.generate_multi_selectable_list_box([])
        self.directory_content.grid(columnspan=2, rowspan=12, column=15, row=0, sticky=W + E + N + S)

        i = 0
        while i < 12:
            Grid.rowconfigure(self, i, weight=1)
            i += 1
        i = 0
        while i < 17:
            Grid.columnconfigure(self, i, weight=1)
            i += 1

    def search_xdcc(self, widget):
        """
        Searches for xdcc packs using the currently selected search engine
        :param widget: the search button
        :return: void
        """
        if widget is not None:
            search_engine = self.search_engine_combo_box.get()
            search_term = self.search_field.get()
            self.search_result = self.conduct_xdcc_search(search_engine, search_term)

            self.clear_list_box(self.search_results)

            i = 0
            for result in self.search_result:
                choice = "#" + str(i) + ": " + result.to_string()
                self.search_results.insert(END, choice)
                i += 1

    def start_download(self, widget):
        """
        Starts the Download
        :param widget: the Download Button
        :return: void
        """
        if widget is None:
            return

        preparation = self.prepare(self.destination.get(),
                                   self.show.get(),
                                   self.season.get(),
                                   self.episode.get(),
                                   self.main_icon_location.get(),
                                   self.secondary_icon_location.get(),
                                   self.method_combo_box.get())
        if len(preparation) != 6:
            self.show_message_dialog(preparation[0], preparation[1])
            return

        directory, show, season, first_episode, special, new_directory = preparation

        selected_packs = self.get_selected_multi_selectable_list_box_elements(self.search_results)
        packs = []
        for key in selected_packs:
            packs.append(self.search_result[key])
        if len(packs) == 0:
            return

        downloader = self.download_engine_combo_box.get()
        files = []
        if downloader == "Hexchat Plugin":
            if self.rename_check.var.get() and not special:
                files = HexChatPluginDownloader(packs, show, first_episode, season).download_loop()
            else:
                files = HexChatPluginDownloader(packs).download_loop()
        elif downloader == "Twisted":
            if self.rename_check.var.get() and not special:
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
        directory = self.destination.get()
        try:
            show_name = directory.rsplit("/", 1)[1]
        except IndexError:
            show_name = directory.rsplit("/", 1)[0]
        self.show.delete(0, END)
        self.search_field.delete(0, END)
        self.show.insert(0, show_name)
        self.search_field.insert(0, show_name + " 1080")

        self.clear_list_box(self.directory_content)
        if os.path.isdir(directory):
            highest_season = 1
            while os.path.isdir(directory + "/Season" + str(highest_season + 1)):
                highest_season += 1
            if os.path.isdir(directory + "/Season " + str(highest_season)):
                children = os.listdir(directory + "/Season " + str(highest_season))
                for child in children:
                    self.directory_content.insert(END, child)
                self.episode.delete(0, END)
                self.season.delete(0, END)
                self.episode.insert(0, str(len(children) + 1))
                self.season.insert(0, str(highest_season))
                main_icon = directory + "/.icons/media_manager.png"
                if os.path.isfile(main_icon):
                    self.main_icon_location.delete(0, END)
                    self.main_icon_location.insert(0, main_icon)
                secondary_icon = directory + "/.icons/Season " + str(highest_season) + ".png"
                if os.path.isfile(secondary_icon):
                    self.secondary_icon_location.delete(0, END)
                    self.secondary_icon_location.insert(0, secondary_icon)

    def browse_for_destination(self, widget):
        """
        Opens a file browser dialog to select a directory to the show's root directory
        :param widget: the button that caused this method call
        :return: void
        """
        if widget is not None:
            directory = self.show_directory_chooser_dialog()
            self.destination.delete(0, END)
            self.destination.insert(0, directory)
