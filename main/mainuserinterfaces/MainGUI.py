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
        hbox = Gtk.Box(spacing=6)
        self.add(hbox)
        while i < len(self.plugins):
            button = Gtk.Button.new_with_label(self.plugins[i].getName())
            button.connect("clicked", self.startPlugin, self.plugins[i])
            hbox.pack_start(button, True, True, 0)
            i += 1

    def startPlugin(self, widget, plugin):
        plugin.startGUI(self)
