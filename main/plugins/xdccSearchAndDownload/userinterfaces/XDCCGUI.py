import os
import configparser
from gi.repository import Gtk
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
        Gtk.Window.__init__(self, title="Main GUI")
        self.set_border_width(10)

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        self.add(grid)

        self.searchResult = []
        self.autorename = False
        self.showname = ""
        self.episodeNumber = 0
        self.seasonNumber = 0

        self.entry = Gtk.Entry()
        self.entry.set_text("Enter Search Term here")
        grid.add(self.entry)

        searchButton = Gtk.Button.new_with_label("Search")
        searchButton.connect("clicked", self.searchXDCC)
        grid.add(searchButton)

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
        grid.add(self.scrollable_treelist)
        self.treeSelection = self.treeview.get_selection()
        self.treeSelection.set_mode(Gtk.SelectionMode.MULTIPLE)

        self.selectionBox = Gtk.ListBox()
        self.selectionBox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        grid.add(self.selectionBox)

        startButton = Gtk.Button.new_with_label("Download")
        startButton.connect("clicked", self.startDownload)
        grid.add(startButton)

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
        self.showname = self.showText.get("1.0", tkinter.END).split("\n")[0]
        self.episodeNumber = int(self.episodeNoText.get("1.0", tkinter.END).split("\n")[0])
        self.seasonNumber = int(self.seasonNoText.get("1.0", tkinter.END).split("\n")[0])
        self.newgui.destroy()
        self.__init__(self.parent)


    """
    Dirty Hack to allow the gui to react to CTRL-a
    """
    #LEGACY TK
    def select_all(self, event):
        self.text.tag_add(tkinter.SEL, "1.0", tkinter.END)
        self.text.mark_set(tkinter.INSERT, "1.0")
        self.text.see(tkinter.INSERT)
        return 'break'