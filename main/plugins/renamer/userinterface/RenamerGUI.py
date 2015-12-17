from tkinter import *
import easygui
from plugins.renamer.utils.Renamer import Renamer

class RenamerGUI(object):

    def __init__(self):
        self.gui = Tk()

        self.button = Button(self.gui, text="Automatic Renaming", command=self.startRename)
        self.button.pack()

        self.text = Text(self.gui)
        self.text.insert(INSERT, "Enter Absolute File Path here")
        self.text.bind("<Control-Key-a>", self.select_all)
        self.text.bind("<Control-Key-A>", self.select_all)
        self.text.bind("<Return>", self.startRename)
        self.text.pack()

    def start(self):
        self.gui.mainloop()
        print("test")

    def startRename(self, dummy=""):
        try:
            absDir = self.text.get("1.0", END).split("\n")[0]
            print(absDir)
            renamer = Renamer(absDir)
            confirmation = renamer.requestConfirmation()
            if self.confirmer(confirmation):
                renamer.confirm(confirmation)
                renamer.startRename()
        except Exception as e:
            if str(e) == "Not a directory": easygui.msgbox(str(e))
            else: raise e

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