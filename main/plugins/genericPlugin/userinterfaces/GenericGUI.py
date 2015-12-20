import tkinter
"""
Generic GUII class defining a kind of interface for GUII construction
"""
class GenericGUI(object):

    """
    Initializes the gui, destroying the parent
    @:param parent - the parent gui
    """
    def __init__(self, parent):
        self.parent = parent
        parent.destroy()
        self.gui = tkinter.Tk()
        self.setUp()

    """
    Sets up the elements of the GUI
    """
    def setUp(self):
        raise NotImplementedError()

    """
    Starts the GUI
    """
    def start(self):
        self.gui.mainloop()


    """
    Stops the gui and restarts the parent
    """
    def stop(self):
        self.gui.destroy()
        self.parent.__init__(self.parent.plugins)