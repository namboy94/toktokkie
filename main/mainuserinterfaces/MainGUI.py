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
        print(activePlugins)
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
        for plugin in self.plugins:
            button = tkinter.Button(self.root, text=plugin.getName(), command=lambda: plugin.startGUI(self))
            button.pack()
            self.buttons.append(button)