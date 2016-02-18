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
from subprocess import Popen

from plugins.batchDownloadManager.searchengines.IntelGetter import IntelGetter
from plugins.batchDownloadManager.searchengines.IxIRCGetter import IxIRCGetter
from plugins.batchDownloadManager.searchengines.NIBLGetter import NIBLGetter
from plugins.batchDownloadManager.downloaders.HexChatPluginDownloader import HexChatPluginDownloader

from guitemplates.gtk.GenericGtkGui import GenericGtkGui
from plugins.batchDownloadManager.downloaders.TwistedDownloader import TwistedDownloader
from plugins.common.fileOps.FileMover import FileMover
from plugins.iconizer.utils.DeepIconizer import DeepIconizer


class BatchDownloadManagerGUI(GenericGtkGui):
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
        self.destination = self.generate_text_entry("", self.on_directory_changed)
        self.grid.attach(self.destination_label, 0, 0, 20, 5)
        self.grid.attach(self.destination, 20, 0, 20, 5)

        self.show_label = self.generate_label("Show Name")
        self.show = self.generate_text_entry("")
        self.grid.attach(self.show_label, 0, 2, 20, 5)
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
            {"#": (int,), "Bot": (str,), "Pack": (int,), "Size": (str,), "Filename": (str,)})
        self.grid.attach(self.search_results["scrollable"], 45, 0, 60, 60)

        self.directory_content = self.generate_multi_list_box({"File Name": (str,)})
        self.grid.attach(self.directory_content["scrollable"], 110, 0, 20, 60)

    def search_xdcc(self, widget):
        """
        Searches for xdcc packs using the currently selected search engine
        :param widget: the search button
        :return: void
        """
        if widget is not None:
            search_engine = self.get_current_selected_combo_box_option(self.search_engine_combo_box)
            search_term = self.search_field.get_text()
            self.search_result = self.xdccSearch(search_engine, search_term, self.search_results["list_store"])

    def start_download(self, widget):
        """
        Starts the Download
        :param widget: the Download Button
        :return: void
        """
        if widget is None:
            return
        preparation = self.prepare()
        if preparation is None:
            return
        directory, show, season, first_episode, special, new_directory = preparation

        packs = self.get_selected(self.search_result, self.search_results["selection"])
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

    def prepare(self):
        """
        Prepares the download
        :return: [the original directory,
                  the show name,
                  the season number,
                  the first episode number,
                  if it's special,
                  and the new directory]
        """
        directory = self.destination.get_text()
        if not directory.endswith("/"):
            directory += "/"
        if os.path.isdir(directory):
            update = True
        else:
            update = False

        show = self.show.get_text()
        if not show:
            self.show_message_dialog("No show name specified")
            return None

        if not self.season.get_text():
            self.show_message_dialog("No Season number specified")
            return None
        try:
            season = int(self.season.get_text())
            special = False
        except ValueError:
            season = self.season.get_text()
            special = True

        if special:
            new_directory = directory + str(season) + "/"
        else:
            new_directory = directory + "Season " + str(season) + "/"

        if not update:
            Popen(["mkdir", "-p", directory]).wait()
            if not os.path.isdir(directory):
                self.show_message_dialog("Error creating directory", "Was a valid directory string entered?")
                return None
            Popen(["mkdir", "-p", directory + ".icons"]).wait()

        season_update = False
        if update and os.path.isdir(new_directory):
            season_update = True

        if not season_update:
            Popen(["mkdir", "-p", new_directory]).wait()

        episodes = os.listdir(new_directory)
        first_episode = len(episodes) + 1

        main_icon = self.main_icon_location.get_text()
        secondary_icon = self.secondary_icon_location.get_text()

        if main_icon:
            if self.get_icon(main_icon, directory + ".icons/", "media_manager.png") == "error":
                self.show_message_dialog("Error retrieving image from source")
                return None
        if secondary_icon:
            if self.get_icon(secondary_icon, directory + ".icons/",
                             new_directory.rsplit("/", 2)[1] + ".png") == "error":
                self.show_message_dialog("Error retrieving image from source")
                return None

        if main_icon or secondary_icon:
            method = self.get_current_selected_combo_box_option(self.method_combo_box)
            DeepIconizer(directory, method).iconize()

        first_ep = self.episode.get_text()
        if first_ep:
            try:
                first_episode = int(first_ep)
            except ValueError:
                self.messageBox("Not a valid episode number")
                return None

        return [directory, show, season, first_episode, special, new_directory]

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
            before = os.listdir()  # This is currently intended
            Popen(["wget", path]).wait()
            after = os.listdir()   # Yes, this too
            new_file = ""
            for file in after:
                if file not in before:
                    new_file = file
                    break
            Popen(["mv", new_file, folder_icon_directory + icon_file]).wait()

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

    @staticmethod
    def xdcc_search(search_engine, search_term, list_store):
        """
        Conducts the XDCC search
        :param search_engine: the search engine to be used
        :param search_term: the search term
        :param list_store: the list store to populate with the results
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

        list_store.clear()
        i = 0
        for result in search_result:
            choice = (i,) + result.toTuple()
            list_store.append(list(choice))
            i += 1

        return search_result
    
    @staticmethod
    def get_selected(search_result, tree_selection):
        """
        Returns the selected elements from the tree selection
        :param search_result: the search result list
        :param tree_selection: the tree selection
        :return: the selection as list of packs
        """
        selected = []
        (model, path_list) = tree_selection.get_selected_rows()
        for path in path_list:
            tree_iter = model.get_iter(path)
            selected.append(model.get_value(tree_iter, 0))
        packs = []
        for selection in selected:
            packs.append(search_result[selection])
        return packs
