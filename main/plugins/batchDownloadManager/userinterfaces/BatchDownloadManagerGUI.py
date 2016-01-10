from gi.repository import Gtk
from plugins.genericPlugin.userinterfaces.GenericGUI import GenericGUI

"""
GUI for the BatchDownloadManager plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class BatchDownloadManagerGUI(GenericGUI):

    """
    Sets up all interface elements of the GUI
    """
    def setUp(self):

        self.destinationLabel = self.generateLabel("Destination Directory")
        self.destination = self.generateEntry("")
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

        self.divider1 = self.generateLabel("")
        self.divider2 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.seasonLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.divider2, self.season, Gtk.PositionType.BOTTOM, 20, 10)

        self.searchLabel = self.generateLabel("Search Term")
        self.searchField = self.generateEntry("")
        self.grid.attach_next_to(self.searchLabel, self.divider1, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.searchField, self.divider2, Gtk.PositionType.BOTTOM, 20, 10)

        self.searchEngineLabel = self.generateLabel("Search Engine")
        self.searchEngineComboBox = self.generateComboBox(["NIBL.co.uk", "ixIRC.com", "intel.haruhichan.com"])
        self.grid.attach_next_to(self.searchEngineLabel, self.searchLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.searchEngineComboBox[0], self.searchField, Gtk.PositionType.BOTTOM, 20, 10)

        self.divider1 = self.generateLabel("")
        self.divider2 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.searchEngineLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.divider2, self.searchEngineComboBox[0], Gtk.PositionType.BOTTOM, 20, 10)

        self.searchButton = self.generateSimpleButton("Start Search", self.dummy)
        self.grid.attach_next_to(self.searchButton, self.divider1, Gtk.PositionType.BOTTOM, 40, 10)

        self.divider3 = self.generateLabel("")
        self.divider4 = self.generateLabel("")
        self.grid.attach_next_to(self.divider3, self.divider1, Gtk.PositionType.BOTTOM, 20, 30)
        self.grid.attach_next_to(self.divider4, self.divider2, Gtk.PositionType.BOTTOM, 20, 30)

        self.downloadEngineLabel = self.generateLabel("Download Engine")
        self.downloadEngineComboBox = self.generateComboBox(["Hexchat Plugin", "External Script"])
        self.grid.attach_next_to(self.downloadEngineLabel, self.divider3, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.downloadEngineComboBox[0], self.divider4, Gtk.PositionType.BOTTOM, 20, 10)

        self.divider1 = self.generateLabel("")
        self.divider2 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.downloadEngineLabel, Gtk.PositionType.BOTTOM, 20, 10)
        self.grid.attach_next_to(self.divider2, self.downloadEngineComboBox[0], Gtk.PositionType.BOTTOM, 20, 10)

        self.downloadButton = self.generateSimpleButton("Start Download", self.dummy)
        self.grid.attach_next_to(self.downloadButton, self.divider1, Gtk.PositionType.BOTTOM, 40, 10)

        self.divider1 = self.generateLabel("")
        self.grid.attach_next_to(self.divider1, self.destination, Gtk.PositionType.RIGHT, 2, 130)

        listStore = Gtk.ListStore(int, str, int, str, str)
        self.searchResults = self.generateMultiListBox(listStore, ["#", "Bot", "Pack", "Size", "Filename"])
        self.grid.attach_next_to(self.searchResults[0], self.divider1, Gtk.PositionType.RIGHT, 70, 130)

    def dummy(self, widget):
        print()