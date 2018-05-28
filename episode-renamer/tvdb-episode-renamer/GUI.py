"""
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of tvdb-episode-renamer.

tvdb-episode-renamer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tvdb-episode-renamer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with tvdb-episode-renamer.  If not, see <http://www.gnu.org/licenses/>.
"""

from tkinter import *
import easygui
from renamer.utils.renamer import Renamer

class GUI(object):

    def __init__(self):
        self.gui = Tk()

        self.button = Button(self.gui, text="Start Renaming", command=self.startRename)
        self.button.pack()

        self.text = Text(self.gui)
        self.text.insert(INSERT, "Enter Absolute File Path here")
        self.text.bind("<Control-Key-a>", self.select_all)
        self.text.bind("<Control-Key-A>", self.select_all)
        self.text.bind("<Return>", self.startRename)
        self.text.pack()

        self.gui.mainloop()

    def startRename(self, dummy=""):
        absDir = self.text.get("1.0", END).split("\n")[0]
        print(absDir)
        renamer = Renamer(absDir)
        confirmation = renamer.requestConfirmation()
        if self.confirmer(confirmation):
            renamer.confirm(confirmation)
            renamer.startRename()

    def confirmer(self, confirmation):
        i = 0
        while i < len(confirmation[0]):
            message = "Rename\n"
            message += confirmation[0][i]
            message += "\nto\n"
            message += confirmation[1][i]
            message += "\n?"
            if not easygui.ynbox(msg=message) == 1:
                return False
            i += 1
        return True

    #LEGACY TK
    def select_all(self, event):
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(INSERT, "1.0")
        self.text.see(INSERT)
        return 'break'