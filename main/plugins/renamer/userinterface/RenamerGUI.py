import tkinter
import easygui
from plugins.renamer.utils.Renamer import Renamer

"""
GUI for the Renamer plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class RenamerGUI(object):

    """
    Constructor
    Sets up all interface elements of the GUI
    """
    def __init__(self):
        self.gui = tkinter.Tk()

        self.button = tkinter.Button(self.gui, text="Automatic Renaming", command=self.startRename)
        self.button.pack(fill=tkinter.X)

        self.text = tkinter.Text(self.gui)
        self.text.insert(tkinter.INSERT, "Enter Absolute File Path here")
        self.text.bind("<Control-Key-a>", self.select_all)
        self.text.bind("<Control-Key-A>", self.select_all)
        self.text.bind("<Return>", self.startRename)
        self.text.pack(fill=tkinter.X)

    """
    Starts the GUI
    """
    def start(self):
        self.gui.mainloop()

    """
    Starts the renaming process
    """
    def startRename(self, dummy=""):
        try:
            absDir = self.text.get("1.0", tkinter.END).split("\n")[0]
            renamer = Renamer(absDir)
            confirmation = renamer.requestConfirmation()
            if self.confirmer(confirmation):
                renamer.confirm(confirmation)
                renamer.startRename()
        except Exception as e:
            if str(e) == "Not a directory": easygui.msgbox(str(e))
            else: raise e

    """
    Asks the user for confirmation before continuing the rename
    """
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

    """
    Dirty Hack to allow the gui to react to CTRL-a
    """
    #LEGACY TK
    def select_all(self, event):
        self.text.tag_add(tkinter.SEL, "1.0", tkinter.END)
        self.text.mark_set(tkinter.INSERT, "1.0")
        self.text.see(tkinter.INSERT)
        return 'break'