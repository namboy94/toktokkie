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
from guitemplates.gtk.GenericGtkGui import GenericGtkGui
from plugins.common.fileOps.FileMover import FileMover
from plugins.xdccSearchAndDownload.userinterfaces.XDCCGUI import XDCCGUI
from plugins.xdccSearchAndDownload.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
from plugins.xdccSearchAndDownload.downloaders.TwistedDownloader import TwistedDownloader
from plugins.iconizer.utils.DeepIconizer import DeepIconizer


class BatchDownloadManagerGUI(GenericGtkGui):
    """
    GUI for the BatchDownloadManager plugin
    """
    
    def __init__(self, parent):
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

    """
    Sets up all interface elements of the GUI
    """
    def lay_out(self):

        self.destination_label = self.generate_label("Destination Directory")
        self.destination = self.generate_entry("", self.on_directory_changed)
        self.destination.connect("changed", )
        self.grid.attach(self.destination_label, 0, 0, 20, 10)
        self.grid.attach(self.destination, 20, 0, 20, 10)

        self.show_label = self.generate_label("Show Name")
        self.show = self.generate_entry("")
        self.grid.attach(self.show_label, 0, 10, 20, 10)
        self.grid.attach(self.show, 20, 10, 20, 10)

        self.season_label = self.generate_label("Season Number")
        self.season = self.generate_entry("")
        self.grid.attach(self.season_label, 0, 20, 20, 10)
        self.grid.attach(self.season, 20, 20, 20, 10)

        self.episode_label = self.generate_label("Starting Episode Number")
        self.episode = self.generate_entry("optional")
        self.grid.attach(self.episode_label, 0, 30, 20, 10)
        self.grid.attach(self.episode, 20, 30, 20, 10)

        self.search_label = self.generate_label("Search Term")
        self.search_field = self.generate_entry("", self.search_xdcc)
        self.grid.attach(self.search_label, 0, 50, 20, 10)
        self.grid.attach(self.search_field, 20, 50, 20, 10)

        self.search_engine_label = self.generate_label("Search Engine")
        self.search_engine_combo_box = self.generate_combo_box(["NIBL.co.uk", "ixIRC.com", "intel.haruhichan.com"])
        self.grid.attach(self.search_engine_label, 0, 60, 20, 10)
        self.grid.attach(self.search_engine_combo_box["combo_box"], 20, 60, 20, 10)

        self.search_button = self.generate_simple_button("Start Search", self.searchXDCC)
        self.grid.attach(self.search_button, 0, 80, 40, 10)

        self.download_engine_label = self.generate_label("Download Engine")
        self.download_engine_combo_box = self.generate_combo_box(["Hexchat Plugin", "Twisted"])
        self.grid.attach(self.download_engine_label, 0, 100, 20, 10)
        self.grid.attach(self.download_engine_combo_box["combo_box"], 20, 100, 20, 10)

        self.options_label = self.generate_label("Options")
        self.rename_check = self.generate_check_box("Automatic Rename", True)
        self.grid.attach(self.options_label, 0, 120, 20, 10)
        self.grid.attach(self.rename_check, 20, 120, 20, 10)

        self.main_icon_label = self.generate_label("Main Icon")
        self.secondary_icon_label = self.generate_label("Season Icon")
        self.main_icon_location = self.generate_entry("")
        self.secondary_icon_location = self.generate_entry("")
        self.method_label = self.generate_label("Method")
        self.method_combo_box = self.generate_combo_box(["Nautilus", "Nemo"])
        self.grid.attach(self.main_icon_label, 0, 140, 20, 10)
        self.grid.attach(self.secondary_icon_label, 0, 150, 20, 10)
        self.grid.attach(self.main_icon_location, 20, 140, 20, 10)
        self.grid.attach(self.secondary_icon_location, 20, 150, 20, 10)
        self.grid.attach(self.method_label, 0, 160, 20, 10)
        self.grid.attach(self.method_combo_box["combo_box"], 20, 160, 20, 10)

        self.download_button = self.generate_simple_button("Start Download", self.start_download)
        self.grid.attach(self.download_button, 0, 180, 40, 10)

        self.search_results = self.generateMultiListBox(
            {"#": int, "Bot": str, "Pack": int, "Size": str, "Filename": str})
        self.grid.attach(self.searchResults["scrollable"], 22, 0, 60, 200)

        self.directory_content = self.generateMultiListBox({"File Name": str})
        self.grid.attach(self.directoryContent["scrollable"], 84, 0, 20, 200)

    """
    """
    def searchXDCC(self, widget):
        searchEngine = self.getCurrentSelectedComboBox(self.searchEngineComboBox)
        searchTerm = self.searchField.get_text()
        self.searchResult = XDCCGUI.xdccSearch(searchEngine, searchTerm, self.searchResults[3])


    """
    """
    def startDownload(self, widget):
        preparation = self.prepare()
        if preparation is None: return
        directory, show, season, firstEpisode, special, newDirectory = preparation

        packs = XDCCGUI.getSelected(self.searchResult, self.searchResults[1])
        downloader = self.getCurrentSelectedComboBox(self.download_engine_combo_box)
        files = []
        if downloader == "Hexchat Plugin":
            if self.rename_check.get_active() and not special:
                files = HexChatPluginDownloader(packs, show, firstEpisode, season).downloadLoop()
            else:
                files = HexChatPluginDownloader(packs).downloadLoop()
        elif downloader == "Twisted":
            if self.rename_check.get_active() and not special:
                files = TwistedDownloader(packs, show, firstEpisode, season).downloadLoop()
            else:
                files = TwistedDownloader(packs).downloadLoop()

        for file in files:
            FileMover.moveFile(file, newDirectory)

    """
    """
    def prepare(self):
        directory = self.destination.get_text()
        if not directory.endswith("/"): directory += "/"
        if os.path.isdir(directory):
            update = True
        else:
            update = False

        show = self.show.get_text()
        if not show:
            self.messageBox("No show name specified")
            return None

        if not self.season.get_text():
            self.messageBox("No Season number specified")
            return None
        try:
            season = int(self.season.get_text())
            special = False
        except Exception:
            season = self.season.get_text()
            special = True

        if special:
            newDirectory = directory + str(season) + "/"
        else:
            newDirectory = directory + "Season " + str(season) + "/"

        if not update:
            Popen(["mkdir", "-p", directory]).wait()
            if not os.path.isdir(directory):
                self.messageBox("Error creating directory", "Was a valid directory string entered?")
                return None
            Popen(["mkdir", "-p", directory + ".icons"]).wait()

        seasonUpdate = False
        if update and os.path.isdir(newDirectory):
            seasonUpdate = True

        if not seasonUpdate:
            Popen(["mkdir", "-p", newDirectory]).wait()

        episodes = os.listdir(newDirectory)
        firstEpisode = len(episodes) + 1

        mainIcon = self.main_icon_location.get_text()
        secondaryIcon = self.secondary_icon_location.get_text()

        if mainIcon:
            if self.getIcon(mainIcon, directory + ".icons/", "main.png") == "error":
                self.messageBox("Error retrieving image from source")
                return None
        if secondaryIcon:
            if self.getIcon(secondaryIcon, directory + ".icons/", newDirectory.rsplit("/", 2)[1] + ".png") == "error":
                self.messageBox("Error retrieving image from source")
                return None

        if mainIcon or secondaryIcon:
            method = self.getCurrentSelectedComboBox(self.method_combo_box)
            DeepIconizer(directory, method).iconize()

        firstEp = self.episode.get_text()
        if firstEp:
            try:
                firstEpisode = int(firstEp)
            except:
                self.messageBox("Not a valid episode number")
                return None

        return [directory, show, season, firstEpisode, special, newDirectory]


    def getIcon(self, path, folderIconDirectory, iconFile):
        if os.path.isfile(path):
            if not path == folderIconDirectory + iconFile:
                if os.path.isfile(folderIconDirectory + iconFile):
                    Popen(["rm", folderIconDirectory + iconFile]).wait()
                Popen(["cp", path, folderIconDirectory + iconFile]).wait()
        else:
            try:
                before = os.listdir()
                Popen(["wget", path]).wait()
                after = os.listdir()
                newFile = ""
                for file in after:
                    if not file in before:
                        newFile = file
                        break
                Popen(["mv", newFile, folderIconDirectory + iconFile]).wait()
            except Exception as e:
                return "error"

    def onDirectoryChanged(self, widget):
        directory = self.destination.get_text()
        showName = ""
        try:
            showName = directory.rsplit("/", 1)[1]
        except:
            showName = directory.rsplit("/", 1)[0]
        self.show.set_text(showName)
        self.searchField.set_text(showName + " 1080")

        self.directoryContent[3].clear()
        if os.path.isdir(directory):
            highestSeason = 1
            while (os.path.isdir(directory + "/Season" + str(highestSeason + 1))): highestSeason += 1
            if os.path.isdir(directory + "/Season " + str(highestSeason)):
                children = os.listdir(directory + "/Season " + str(highestSeason))
                for child in children:
                    self.directoryContent[3].append([child])
                self.episode.set_text(str(len(children) + 1))
                self.season.set_text(str(highestSeason))
                mainIcon = directory + "/.icons/main.png"
                if os.path.isfile(mainIcon):
                    self.main_icon_location.set_text(mainIcon)
                secondaryIcon = directory + "/.icons/Season " + str(highestSeason) + ".png"
                if os.path.isfile(secondaryIcon):
                    self.secondary_icon_location.set_text(secondaryIcon)

