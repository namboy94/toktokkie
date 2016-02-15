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

import configparser
import os

from gi.repository import Gtk
from plugins.genericPlugin.userinterfaces.GenericGUI import GenericGUI
from plugins.xdccSearchAndDownload.downloaders.HexChatPluginDownloader import HexChatPluginDownloader

from plugins.batchDownloadManager.searchengines.downloaders.TwistedDownloader import TwistedDownloader

"""
GUI for the XDCC Search and Download class
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class XDCCGUI(GenericGUI):

    """
    Initializes the interface elements
    """
    def setUp(self):
        self.searchResult = []
        self.autorename = False
        self.showname = ""
        self.episodeNumber = 0
        self.seasonNumber = 0

        self.entry = Gtk.Entry()
        self.entry.set_text("Enter Search Term here")
        self.entry.connect("key-press-event", self.defaultEnterKey)
        self.grid.attach(self.entry, 0, 0, 2, 2)

        self.searchEngines = Gtk.ListStore(str)
        self.searchEngines.append(("NIBL.co.uk",))
        self.searchEngines.append(("Intel Haruhichan",))
        self.searchEngines.append(("ixIRC",))
        self.searchEngine = Gtk.ComboBox.new_with_model(self.searchEngines)
        renderer_text = Gtk.CellRendererText()
        self.searchEngine.pack_start(renderer_text, True)
        self.searchEngine.add_attribute(renderer_text, "text", 0)
        self.searchEngine.set_active(0)
        self.grid.attach_next_to(self.searchEngine, self.entry, Gtk.PositionType.RIGHT, 1, 1)

        self.searchButton = Gtk.Button.new_with_label("Search")
        self.searchButton.connect("clicked", self.searchXDCC)
        self.grid.attach_next_to(self.searchButton, self.searchEngine, Gtk.PositionType.BOTTOM, 1, 1)

        self.listStore = Gtk.ListStore(int, str, int, str, str)
        self.treeview = Gtk.TreeView.new_with_model(self.listStore.filter_new())
        for i, column_title in enumerate(["#", "Bot", "Pack", "Size", "Filename"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.add(self.treeview)
        self.treeSelection = self.treeview.get_selection()
        self.treeSelection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.grid.attach_next_to(self.scrollable_treelist, self.entry, Gtk.PositionType.BOTTOM, 3, 5)

        self.startButton = Gtk.Button.new_with_label("Download")
        self.startButton.connect("clicked", self.startDownload)
        self.grid.attach_next_to(self.startButton, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)


    """
    Conducts a search for the currently entered search term
    """
    def searchXDCC(self, widget):
        search = self.searchEngines.get(self.searchEngine.get_active_iter(), 0)
        searchTerm = self.entry.get_text()
        self.searchResult = XDCCGUI.xdccSearch(search[0], searchTerm, self.listStore)

    """
    Starts the download of the selected packs
    """
    def startDownload(self, widget):
        packs = XDCCGUI.getSelected(self.searchResult, self.treeSelection)
        self.promptAutoRename()
        config = configparser.ConfigParser()
        config.read((os.getenv("HOME") + "/.mediamanager/configs/mainconfig"))
        downloader = dict(config.items("defaults"))["downloader"]
        if downloader == "twisted":
            if self.autorename:
                TwistedDownloader(packs, self.showname, self.episodeNumber, self.seasonNumber).downloadLoop()
            else:
                TwistedDownloader(packs).downloadLoop()
        elif downloader == "hexchat":
            if self.autorename:
                HexChatPluginDownloader(packs, self.showname, self.episodeNumber, self.seasonNumber).downloadLoop()
            else:
                HexChatPluginDownloader(packs, self.showname).downloadLoop()
    """
    Asks the user
    """
    def promptAutoRename(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Auto Rename File?")
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            #self.autorename = True
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Sorry, not implemented yet")
            dialog.run()
            dialog.destroy()

    """
    Sets the variables for the autorename
    """
    def autorenamebutton(self):
        print("TODO")



    ###STATIC METHODS###
    @staticmethod


