import tkinter
from subprocess import Popen
from plugins.common.onlineDataGetters.NIBLGetter import NIBLGetter

class XDCCGUI(object):

    def __init__(self):
        self.gui = tkinter.Tk()
        self.searchResult = []

        self.searchButton = tkinter.Button(self.gui, text="Search", command=self.searchXDCC, width=50)
        self.searchButton.pack()
        self.startButton = tkinter.Button(self.gui, text="Start", command=self.startDownload, width=50)
        self.startButton.pack()

        self.text = tkinter.Text(self.gui, width=100, height=3)
        self.text.insert(tkinter.INSERT, "Enter Search Term here")
        self.text.bind("<Control-Key-a>", self.select_all)
        self.text.bind("<Control-Key-A>", self.select_all)
        self.text.pack()

        self.box = tkinter.Listbox(self.gui, selectmode=tkinter.EXTENDED, width=100)
        self.box.pack()

    def start(self):
        self.gui.mainloop()

    def searchXDCC(self):
        searchTerm = self.text.get("1.0", tkinter.END).split("\n")[0]
        self.searchResult = NIBLGetter(searchTerm).search()
        for result in self.searchResult:
            choice = result[0] + " - " + result[1] + " - " + result[3]
            self.box.insert(tkinter.END, choice)

    def startDownload(self):
        items = self.box.curselection()
        for item in items:
            Popen(["ls", "-a"])
            p = Popen(["python2", "/home/hermann/IDEs/Projects/PyCharm/media-manager/main/external/xdccbot.py", "irc.rizon.net", "horriblesubs", "asuhdashdsadsad", self.searchResult[item][1], self.searchResult[item][2]])
            print(p.communicate())
            print(str(item))


    #LEGACY TK
    def select_all(self, event):
        self.text.tag_add(tkinter.SEL, "1.0", tkinter.END)
        self.text.mark_set(tkinter.INSERT, "1.0")
        self.text.see(tkinter.INSERT)
        return 'break'