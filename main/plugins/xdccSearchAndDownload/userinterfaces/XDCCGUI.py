import tkinter
from subprocess import Popen
from plugins.common.onlineDataGetters.NIBLGetter import NIBLGetter
from plugins.genericPlugin.userinterfaces.GenericGUI import GenericGUI
import easygui

"""
GUI for the XDCC Search and Download class
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class XDCCGUI(GenericGUI):

    """
    Constructor
    Initializes the interface elements
    """
    def __init__(self):
        self.gui = tkinter.Tk()
        self.searchResult = []

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

    """
    Starts the GUI
    """
    def start(self):
        self.gui.mainloop()

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
        for item in items:
            Popen(["python2", "/home/hermann/IDEs/Projects/PyCharm/media-manager/main/external/xdccbot.py", "irc.rizon.net", "horriblesubs", "asuhdashdsadsad", self.searchResult[item][1], self.searchResult[item][2]])

    """
    Dirty Hack to allow the gui to react to CTRL-a
    """
    #LEGACY TK
    def select_all(self, event):
        self.text.tag_add(tkinter.SEL, "1.0", tkinter.END)
        self.text.mark_set(tkinter.INSERT, "1.0")
        self.text.see(tkinter.INSERT)
        return 'break'