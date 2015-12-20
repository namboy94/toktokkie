import os
import tkinter
import configparser
import easygui
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

        self.text = tkinter.Text(self.gui, width=100, height=3)
        self.text.insert(tkinter.INSERT, "Enter Search Term here")
        self.text.bind("<Control-Key-a>", self.select_all)
        self.text.bind("<Control-Key-A>", self.select_all)
        self.text.pack(fill=tkinter.X)

        self.searchButton = tkinter.Button(self.gui, text="Search", command=self.searchXDCC, width=50)
        self.searchButton.pack(fill=tkinter.X)

        self.box = tkinter.Listbox(self.gui, selectmode=tkinter.EXTENDED, width=100)
        self.box.pack(fill=tkinter.X)

        self.startButton = tkinter.Button(self.gui, text="Download", command=self.startDownload, width=50)
        self.startButton.pack(fill=tkinter.X)
        #TODO Implement that X runs the stop() command

    """
    Conducts a search for the currently entered search term
    """
    def searchXDCC(self):
        searchTerm = self.text.get("1.0", tkinter.END).split("\n")[0]
        self.searchResult = NIBLGetter(searchTerm).search()
        self.box.delete(0, tkinter.END)
        for result in self.searchResult:
            choice = result.toString()
            self.box.insert(tkinter.END, choice)

    """
    Starts the download of the selected packs
    """
    def startDownload(self):
        items = self.box.curselection()
        packs = []
        for item in items:
            packs.append(self.searchResult[item])
        self.promptAutoRename()
        config = configparser.ConfigParser().read((os.getenv("HOME") + "/.mediamanager/configs/mainconfig"))
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
        if easygui.ynbox("Auto Rename File?", "Auto Rename"):
            self.gui.destroy()
            self.autorename = True
            self.newgui = tkinter.Tk()
            showLabel = tkinter.Label(self.newgui, text="Show Name")
            self.showText = tkinter.Text(self.newgui, height=3)
            episodeNoLabel = tkinter.Label(self.newgui, text="(Starting) Episode Number")
            self.episodeNoText = tkinter.Text(self.newgui, height=3)
            seasonNoLabel = tkinter.Label(self.newgui, text="Season Number")
            self.seasonNoText = tkinter.Text(self.newgui, height=3)
            confirmButton = tkinter.Button(self.newgui, text="Start", command=self.autorenamebutton)
            showLabel.pack(fill=tkinter.X)
            self.showText.pack(fill=tkinter.X)
            episodeNoLabel.pack(fill=tkinter.X)
            self.episodeNoText.pack(fill=tkinter.X)
            seasonNoLabel.pack(fill=tkinter.X)
            self.seasonNoText.pack(fill=tkinter.X)
            confirmButton.pack(fill=tkinter.X)
            self.newgui.mainloop()

    """
    Sets the variables for the autorename
    """
    def autorenamebutton(self):
        self.showname = self.showText.get("1.0", tkinter.END).split("\n")[0]
        self.episodeNumber = int(self.episodeNoText.get("1.0", tkinter.END).split("\n")[0])
        self.seasonNumber = int(self.seasonNoText.get("1.0", tkinter.END).split("\n")[0])
        self.newgui.destroy()
        self.__init__()


    """
    Dirty Hack to allow the gui to react to CTRL-a
    """
    #LEGACY TK
    def select_all(self, event):
        self.text.tag_add(tkinter.SEL, "1.0", tkinter.END)
        self.text.mark_set(tkinter.INSERT, "1.0")
        self.text.see(tkinter.INSERT)
        return 'break'