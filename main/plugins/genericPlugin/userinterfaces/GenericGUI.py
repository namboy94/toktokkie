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
    def defaultEnterKey(self, widget, command):
        def enter(wid, ev, com):
            if ev.keyval == Gdk.KEY_Return:
                com(wid)
        widget.connect("key-press-event", enter, command)

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

    """
    Generates a label with predefined text
    @:param labetext - the text to be displayed
    @:return the generated label
    """
    def generateLabel(self, labeltext):
        label = Gtk.Label()
        label.set_text(labeltext)
        return label

    """
    Generates a simple button that executes a specific function
    @:param buttontext - the text to be displayed on the button
    @:param command - the command to be executed
    @:return the generated button
    """
    def generateSimpleButton(self, buttontext, command):
        button = Gtk.Button.new_with_label(buttontext)
        button.connect("clicked", command)
        return button

    """
    Generates a text entry
    @:param defaulttext - the text to be displayed in the netry as default
    @:param command - the command to be executed if the entry is in focus an the Enter/Return key is pressed
    """
    def generateEntry(self, defaulttext, command=None):
        entry = Gtk.Entry()
        entry.set_text(defaulttext)
        if not command is None:
            entry.connect("key-press-event", self.defaultEnterKey, command)
        return entry

    """
    generates a combobox
    @:param options - list of strings that contain the different options the combobox can have
    @:return list of components of the combobox
        0: the combobox object
        1: the ListStore object containing the possible options of the combo box
    """
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

    """
    Generates a multi list box
    @:param listStore - the ListStore object containing the options
    @:param titles - the titles of the columns of the multi list box
    @:return the multi list box as a list of components
        0: the scrollable treelist object
        1: the treeselection
        2: the treeview
        3: the listStore
    """
    def generateMultiListBox(self, listStore, titles):
        treeview = Gtk.TreeView.new_with_model(listStore.filter_new())
        for i, column_title in enumerate(titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            treeview.append_column(column)
        scrollable_treelist = Gtk.ScrolledWindow()
        scrollable_treelist.set_vexpand(True)
        scrollable_treelist.add(treeview)
        treeSelection = treeview.get_selection()
        treeSelection.set_mode(Gtk.SelectionMode.MULTIPLE)
        return [scrollable_treelist, treeSelection, treeview, listStore]

    def generateRadioButton(self, text):
        radio = Gtk.RadioButton.new_with_label(None, text)
        return radio

    def generateCheckBox(self, text, active):
        checkBox = Gtk.CheckButton.new_with_label(text)
        if active:
            checkBox.set_active(True)
        return checkBox

    ###Bequemlichkeitsmethoden###

    """
    @:return the currently selected string of a combobox
    """
    def getCurrentSelectedComboBox(self, comboBoxList):
        return comboBoxList[1].get(comboBoxList[0].get_active_iter(), 0)[0]