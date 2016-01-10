from gi.repository import Gtk, Gdk

"""
Generic GUI class defining a kind of interface for GUII construction
"""
class GenericGUI(Gtk.Window):

    """
    Initializes the gui, destroying the parent
    @:param parent - the parent gui
    """
    def __init__(self, parent, title):
        Gtk.Window.__init__(self, title=title)
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

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



    ###Default Methods###

    """
    Defines the default behaviour when pressing enter for the search entry
    It will act as if pressing the "Search" button
    """
    def defaultEnterKey(self, widget, ev, command):
        if ev.keyval == Gdk.KEY_Return:
            command(widget)

    """
    Opens a message box popup.
    @:param primaryMessage - the primary message to be displayed
    @:param secondaryMessage - the secondary message(subtext) to be displayed
    """
    def messageBox(self, primaryMessage, secondaryMessage=""):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, primaryMessage)
        dialog.format_secondary_text(secondaryMessage)
        dialog.run()
        dialog.destroy()


    ###Generating Methods###


    def generateLabel(self, labeltext):
        label = Gtk.Label()
        label.set_text(labeltext)
        return label

    def generateSimpleButton(self, buttontext, command):
        button = Gtk.Button.new_with_label(buttontext)
        button.connect("clicked", command)
        return button

    def generateEntry(self, defaulttext, command):
        entry = Gtk.Entry()
        entry.set_text(defaulttext)
        entry.connect("key-press-event", self.defaultEnterKey, command)
        return entry

    def generateComboBox(self, options):
        optionStore = Gtk.ListStore(str)
        for option in options:
            optionStore.append((option,))

        comboBox = Gtk.ComboBox.new_with_model(optionStore)
        renderer_text = Gtk.CellRendererText()
        comboBox.pack_start(renderer_text, True)
        comboBox.add_attribute(renderer_text, "text", 0)
        comboBox.set_active(0)

        return [comboBox, optionStore]


    ###Bequemlichkeitsmethoden###

    def getCurrentSelectedComboBox(self, comboBoxList):
        return comboBoxList[1].get(comboBoxList[0].get_active_iter(), 0)[0]