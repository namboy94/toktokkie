import os
import configparser
from gi.repository import Gtk, Gdk
from plugins.common.onlineDataGetters.NIBLGetter import NIBLGetter
from plugins.genericPlugin.userinterfaces.GenericGUI import GenericGUI
from plugins.xdccSearchAndDownload.downloaders.HexChatPluginDownloader import HexChatPluginDownloader
from plugins.xdccSearchAndDownload.downloaders.TwistedDownloader import TwistedDownloader

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
        self.grid.attach(self.entry, 0, 0, 2, 1)

        self.searchButton = Gtk.Button.new_with_label("Search")
        self.searchButton.connect("clicked", self.searchXDCC)
        self.grid.attach_next_to(self.searchButton, self.entry, Gtk.PositionType.RIGHT, 1, 1)

        #Bot - Pack - Size - FileName
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
        self.grid.attach(self.scrollable_treelist, 0, 2, 3, 5)

        startButton = Gtk.Button.new_with_label("Download")
        startButton.connect("clicked", self.startDownload)
        self.grid.attach(startButton, 1, 8, 1, 1)

    """
    Conducts a search for the currently entered search term
    """
    def searchXDCC(self, widget):
        searchTerm = self.entry.get_text()
        self.searchResult = NIBLGetter(searchTerm).search()

        self.listStore.clear()
        i = 0
        for result in self.searchResult:
            choice = (i,) + result.toTuple()
            self.listStore.append(list(choice))
            i += 1

    """
    Starts the download of the selected packs
    """
    def startDownload(self, widget):
        selected = []
        (model, pathlist) = self.treeSelection.get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            selected.append(model.get_value(tree_iter, 0))
        packs = []
        for selection in selected:
            packs.append(self.searchResult[selection])
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

    """
    Defines the default behaviour when pressing enter for the search entry
    It will act as if pressing the "Search" button
    """
    def defaultEnterKey(self, widget, ev):
        if ev.keyval == Gdk.KEY_Return:
            self.searchXDCC(widget)