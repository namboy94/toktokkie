"""
GUI
Class that implements a simple GUI for entering data relevant to the files to be renamed

Created on June 9, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports
from Tkinter import Tk

"""
The Main GUI Class
"""
class InputGUI(object):

    """
    Constructor fo the GUI
    """
    def __init__(self):
        print ""
        
    """
    starts the GUI
    """
    def guiStart(self):
        
        #Initialize GUI
        self.gui = Tk()
        self.gui.geometry("450x500+300+300")
        self.gui.title("Episode Renamer")
        self.gui.wm_resizable(False, False)
        
        #Start GUI
        self.gui.mainloop()