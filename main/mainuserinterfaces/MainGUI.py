from gi.repository import Gtk

"""
Class that implements the Main GUI
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class MainGUI(Gtk.Window):

    """
    Constructor
    """
    def __init__(self, activePlugins):
        Gtk.Window.__init__(self, title="Main GUI")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.plugins = activePlugins
        self.buttons = []
        self.__addButtons__()

    """
    Starts the user interface
    """
    def start(self):
        self.window = self
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()
        Gtk.main()

    """
    Adds buttons for all plugins
    """
    def __addButtons__(self):
        i = 0
        row = 0
        column = -1
        while i < len(self.plugins):
            if i % 3 == 0 and not i == 0: row += 1; column = 0
            else: column += 1
            button = Gtk.Button.new_with_label(self.plugins[i].getName())
            button.connect("clicked", self.startPlugin, self.plugins[i])
            self.grid.attach(button, column, row, 1, 1)
            i += 1

    def startPlugin(self, widget, plugin):
        plugin.startGUI(self)
