from gi.repository import Gtk

"""
Generic GUI class defining a kind of interface for GUII construction
"""
class GenericGUI(Gtk.Window):

    """
    Initializes the gui, destroying the parent
    @:param parent - the parent gui
    """
    def __init__(self, parent):
        self.parent = parent
        self.setUp()

    """
    Sets up the elements of the GUI
    """
    @classmethod
    def setUp(self):
        raise NotImplementedError()

    """
    Starts the GUI
    """
    def start(self):
        #self.parent.window.destroy()
        self.parent.window.hide()
        self.window = self
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()
        Gtk.main()
        self.parent.window.show_all()
