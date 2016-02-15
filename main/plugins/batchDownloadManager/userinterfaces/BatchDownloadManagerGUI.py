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
from subprocess import Popen, PIPE
from gi.repository import Gtk
from plugins.common.fileOps.FileMover import FileMover
from plugins.genericPlugin.userinterfaces.GenericGUI import GenericGUI
from plugins.xdccSearchAndDownload.userinterfaces.XDCCGUI import XDCCGUI
from plugins.xdccSearchAndDownload.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
from plugins.xdccSearchAndDownload.downloaders.TwistedDownloader import TwistedDownloader
from plugins.iconizer.utils.DeepIconizer import DeepIconizer

"""
GUI for the BatchDownloadManager plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class BatchDownloadManagerGUI(GenericGUI):

    """
    Sets up all interface elements of the GUI
    """
    def setUp(self):

        self.searchResult = []

        self.destinationLabel = self.generateLabel("Destination Directory")
        self.destination = self.generateEntry("")
        self.destination.connect("changed", self.onDirectoryChanged)
        self.grid.attach(self.destinationLabel, 0, 0, 20, 10)
        self.grid.attach(self.destination, 20, 0, 20, 10)

        self.showLabel = self.generateLabel("Show Name")
        self.show = self.generateEntry("")
        self.grid.attach_next_to(self.showLabel, self.destinationLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.show, self.destination, Gtk.PositionType.BOTTOM, 20, 10)

        self.seasonLabel = self.generateLabel("Season Number")
        self.season = self.generateEntry("")
        self.grid.attach_next_to(self.seasonLabel, self.showLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.season, self.show, Gtk.PositionType.BOTTOM, 20, 10)

        self.episodeLabel = self.generateLabel("Starting Episode Number")
        self.episode = self.generateEntry("optional")
        self.grid.attach_next_to(self.episodeLabel, self.seasonLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.episode, self.episodeLabel, Gtk.PositionType.RIGHT, 20, 10)

        self.divider1 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.episodeLabel, Gtk.PositionType.BOTTOM, 20, 10)

        self.searchLabel = self.generateLabel("Search Term")
        self.searchField = self.generateEntry("")
        self.defaultEnterKey(self.searchField, self.searchXDCC)
        self.grid.attach_next_to(self.searchLabel, self.divider1, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.searchField, self.searchLabel, Gtk.PositionType.RIGHT, 20, 10)

        self.searchEngineLabel = self.generateLabel("Search Engine")
        self.searchEngineComboBox = self.generateComboBox(["NIBL.co.uk", "ixIRC.com", "intel.haruhichan.com"])
        self.grid.attach_next_to(self.searchEngineLabel, self.searchLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.searchEngineComboBox[0], self.searchField, Gtk.PositionType.BOTTOM, 20, 10)

        self.divider1 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.searchEngineLabel, Gtk.PositionType.BOTTOM, 20, 10)

        self.searchButton = self.generateSimpleButton("Start Search", self.searchXDCC)
        self.grid.attach_next_to(self.searchButton, self.divider1, Gtk.PositionType.BOTTOM, 40, 10)

        self.divider2 = self.generateLabel("")
        self.grid.attach_next_to(self.divider2, self.divider1, Gtk.PositionType.BOTTOM, 20, 30)

        self.downloadEngineLabel = self.generateLabel("Download Engine")
        self.downloadEngineComboBox = self.generateComboBox(["Hexchat Plugin", "Twisted"])
        self.grid.attach_next_to(self.downloadEngineLabel, self.divider2, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.downloadEngineComboBox[0], self.downloadEngineLabel, Gtk.PositionType.RIGHT, 20, 10)

        self.divider1 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.downloadEngineLabel, Gtk.PositionType.BOTTOM, 20, 10)

        self.optionsLabel = self.generateLabel("Options")
        self.renameCheck = self.generateCheckBox("Automatic Rename", True)
        self.grid.attach_next_to(self.optionsLabel, self.divider1, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.renameCheck, self.optionsLabel, Gtk.PositionType.RIGHT, 20, 10)

        self.divider1 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.optionsLabel, Gtk.PositionType.BOTTOM, 20, 10)

        self.mainIconLabel = self.generateLabel("Main Icon")
        self.secondaryIconLabel = self.generateLabel("Season Icon")
        self.mainIconLocation = self.generateEntry("")
        self.secondaryIconLocation = self.generateEntry("")
        self.methodLabel = self.generateLabel("Method")
        self.methodComboBox = self.generateComboBox(["Nautilus", "Nemo"])
        self.grid.attach_next_to(self.mainIconLabel, self.divider1, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.secondaryIconLabel, self.mainIconLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.mainIconLocation, self.mainIconLabel, Gtk.PositionType.RIGHT, 20, 10)
        self.grid.attach_next_to(self.secondaryIconLocation, self.secondaryIconLabel, Gtk.PositionType.RIGHT, 20, 10)
        self.grid.attach_next_to(self.methodLabel, self.secondaryIconLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.methodComboBox[0], self. secondaryIconLocation, Gtk.PositionType.BOTTOM, 20, 10)

        self.divider1 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.methodLabel, Gtk.PositionType.BOTTOM, 20, 10)

        self.downloadButton = self.generateSimpleButton("Start Download", self.startDownload)
        self.grid.attach_next_to(self.downloadButton, self.divider1, Gtk.PositionType.BOTTOM, 40, 10)

        self.divider1 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.destination, Gtk.PositionType.RIGHT, 2, 200)

        listStore = Gtk.ListStore(int, str, int, str, str)
        self.searchResults = self.generateMultiListBox(listStore, ["#", "Bot", "Pack", "Size", "Filename"])
        self.grid.attach_next_to(self.searchResults[0], self.divider1, Gtk.PositionType.RIGHT, 60, 200)

        self.divider1 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.searchResults[0], Gtk.PositionType.RIGHT, 2, 200)

        directoryContentListStore = Gtk.ListStore(str)
        self.directoryContent = self.generateMultiListBox(directoryContentListStore, ["File Name"])
        self.grid.attach_next_to(self.directoryContent[0], self.divider1, Gtk.PositionType.RIGHT, 20, 200)

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
        downloader = self.getCurrentSelectedComboBox(self.downloadEngineComboBox)
        files = []
        if downloader == "Hexchat Plugin":
            if self.renameCheck.get_active() and not special:
                files = HexChatPluginDownloader(packs, show, firstEpisode, season).downloadLoop()
            else:
                files = HexChatPluginDownloader(packs).downloadLoop()
        elif downloader == "Twisted":
            if self.renameCheck.get_active() and not special:
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

        mainIcon = self.mainIconLocation.get_text()
        secondaryIcon = self.secondaryIconLocation.get_text()

        if mainIcon:
            if self.getIcon(mainIcon, directory + ".icons/", "main.png") == "error":
                self.messageBox("Error retrieving image from source")
                return None
        if secondaryIcon:
            if self.getIcon(secondaryIcon, directory + ".icons/", newDirectory.rsplit("/", 2)[1] + ".png") == "error":
                self.messageBox("Error retrieving image from source")
                return None

        if mainIcon or secondaryIcon:
            method = self.getCurrentSelectedComboBox(self.methodComboBox)
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
                    self.mainIconLocation.set_text(mainIcon)
                secondaryIcon = directory + "/.icons/Season " + str(highestSeason) + ".png"
                if os.path.isfile(secondaryIcon):
                    self.secondaryIconLocation.set_text(secondaryIcon)

