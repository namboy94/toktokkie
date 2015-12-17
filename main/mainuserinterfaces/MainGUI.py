import tkinter

"""
Class that implements the Main GUI
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class MainGUI(object):

    """
    Constructor
    """
    def __init__(self, activePlugins):
        self.plugins = activePlugins
        self.buttons = []

        self.root = tkinter.Tk()
        self.__addButtons__()

    """
    Starts the user interface
    """
    def start(self):
        self.root.mainloop()

    """
    Adds buttons for all plugins
    """
    def __addButtons__(self):
        i = 0
        while i < len(self.plugins):
            button = tkinter.Button(self.root, text=self.plugins[i].getName(),
                                    command=lambda i=i: self.plugins[i].startGUI(self))
            button.pack(fill=tkinter.X)
            self.buttons.append(button)
            i += 1