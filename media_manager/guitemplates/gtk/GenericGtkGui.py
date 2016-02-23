"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf


class GenericGtkGui(Gtk.Window):
    """
    Class that models a generic grid-based GTK Gui. This should be used like an
    abstract class from which other classes can inherit from.
    """

    def __init__(self, title="Media Manager", parent=None, hide_parent=True):
        """
        Constructor which initializes the GUI
        :param title: The window title. Defaults to "Finance Manager"
        :param parent: The parent GUI window, provided one wants this Window
                        to have a parent, otherwise it defaults to None
        :param hide_parent: flag that determines if the parent GUI only freezes or is
                        hidden while this window is open
        :return: void
        """
        # object variables
        self.grid = None
        self.window = None
        self.parent = None
        self.hide_parent = False

        self.parent = parent
        self.hide_parent = hide_parent

        # initialize GTK
        # noinspection PyCallByClass
        Gtk.Window.__init__(self, title=title)
        self.set_border_width(10)

        # Set up Grid Layout
        self.grid = Gtk.Grid(column_homogeneous=True,
                             row_homogeneous=False,
                             column_spacing=0,
                             row_spacing=0)
        self.add(self.grid)

        # Delegated to the child classes
        self.lay_out()

    def lay_out(self):
        """
        Abstract method that adds objects to the GUI and places them into the layout.
        :raise NotImplementedError to indicate that this class is abstract
        :return: void
        """
        raise NotImplementedError("lay_out method not implemented")

    def start(self):
        """
        Starts the GUI and enters the gui mainloop. If this window has a parent,
        it will be hidden during the mainloop and reappear at the end
        :return: void
        """
        if self.parent and self.hide_parent:
            self.parent.window.hide()
        self.window = self
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()
        Gtk.main()
        if self.parent and self.hide_parent:
            self.parent.window.show_all()

    # Helper methods

    @staticmethod
    def default_enter_key(widget, command, *additional_args):
        """
        Connects a command to the enter key for a GTK widget.
        This means, if the enter/return key is pressed while the widget is in focus,
        this command will be called.
        :param widget: the widget to which the command should be connected to
        :param command: the command to be executed when pressing the enter key
        :return: void
        """

        def enter(internal_widget, event, internal_command, *more_args):
            """
            Method that evaluates whenever a key is pressed if it's the enter key.
            :param internal_widget: the widget to which this methods listens
            :param event: the key-press event to be evaluated
            :param internal_command: the command to be executed when pressing the enter key
            :return: void
            """
            if event.keyval == Gdk.KEY_Return:
                internal_command(internal_widget, more_args)

        widget.connect("key-press-event", enter, command, additional_args)

    def show_message_dialog(self, primary_message, secondary_message=""):
        """
        Opens a message box displaying a primary and a secondary message
        :param primary_message: the primary message to be displayed
        :param secondary_message: the secondary message to be displayed
        :return: void
        """
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, primary_message)
        dialog.format_secondary_text(secondary_message)
        dialog.run()
        dialog.destroy()

    def show_y_n_dialog(self, primary_message, secondary_message=""):
        """
        Opens a yes/no dialog
        :param primary_message: the primary message to be displayed
        :param secondary_message: the secondary message to be displayed
        :return: True, if yes was selected, False otherwise
        """
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, primary_message)
        dialog.format_secondary_text(secondary_message)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            return True
        else:
            return False

    def show_file_chooser_dialog(self):
        """
        Creates a file chooser dialog
        :return: the selected file path
        """
        dialog = Gtk.FileChooserDialog("Please choose a file", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        selected_file = ""
        if response == Gtk.ResponseType.OK:
            selected_file = dialog.get_filename()
        dialog.destroy()
        return selected_file

    def show_directory_chooser_dialog(self):
        """
        Creates a directory chooser dialog
        :return: the selected directory path
        """
        dialog = Gtk.FileChooserDialog("Please choose a file", self, Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        directory = ""
        if response == Gtk.ResponseType.OK:
            directory = dialog.get_filename()
        dialog.destroy()
        return directory

    def show_text_box(self, message):
        """
        Shows a text box and retrieves a value entered by the user
        :param message: The message addressed to the user to be displayed
        :return: the entered string
        """
        dialog = Gtk.MessageDialog(self, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                   Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, message)
        dialog_box = dialog.get_content_area()
        user_entry = Gtk.Entry()
        user_entry.set_size_request(250, 0)
        dialog_box.pack_end(user_entry, False, False, 0)

        dialog.show_all()

        response = dialog.run()
        response_text = user_entry.get_text()
        dialog.destroy()
        if (response == Gtk.ResponseType.OK) and (response_text != ''):
            return response_text
        else:
            return None

    @staticmethod
    def generate_label(label_text):
        """
        Generates a GTK Label
        :param label_text: the text to be displayed on the label
        :return: the Label object
        """
        label = Gtk.Label()
        label.set_text(label_text)
        return label

    @staticmethod
    def generate_image_label(label_image, width=None, height=None):
        """
        Generates a GTK Image Label
        :param width: the width of the image. If not specified, the default is used
        :param height: the height of the image. If not specified, the default is used
        :param label_image: the image to be displayed on the label
        :return: the Label object
        """
        if height is not None and width is not None:
            print("resize")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(label_image)
            pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
            return Gtk.Image.new_from_pixbuf(pixbuf)
        else:
            return Gtk.Image.new_from_file(label_image)

    @staticmethod
    def generate_simple_button(button_text, command, *additional_args):
        """
        Generates a GTK Button
        :param button_text: the text to be displayed on the button
        :param command: the command to be executed when pressing this button
        :param additional_args: additional arguments to be passed to the command
        :return: the Button object
        """
        button = Gtk.Button.new_with_label(button_text)
        if len(additional_args) == 0:
            button.connect("clicked", command)
        else:
            button.connect("clicked", command, additional_args)
        return button

    @staticmethod
    def generate_text_entry(defaulttext="", command=None, *additional_args):
        """
        Generates a GTK Text Entry
        :param defaulttext: The text to be displayed by default
        :param command: The command to be executed if the enter key is pressed when this
                        text entry is in focus.
        :param additional_args: additional arguments to be passed to the command
        :return: the Entry object
        """
        entry = Gtk.Entry()
        entry.set_text(defaulttext)
        if command is not None:
            entry.connect("key-press-event", GenericGtkGui.default_enter_key, command, additional_args)
        return entry

    @staticmethod
    def generate_combo_box(options):
        """
        Generates a combo box with a given amount of options
        :param options: a list of (string) options to be displayed
        :return: a dictionary with the individual parts of the combo box
                    combo_box: the Combo Box object
                    list_store: the ListStore object that stores the options for the combo box
        """
        option_store = Gtk.ListStore(str)
        for option in options:
            option_store.append((option,))
        combo_box = Gtk.ComboBox.new_with_model(option_store)
        renderer_text = Gtk.CellRendererText()
        combo_box.pack_start(renderer_text, True)
        combo_box.add_attribute(renderer_text, "text", 0)
        combo_box.set_active(0)
        return {"combo_box": combo_box, "list_store": option_store}

    @staticmethod
    def generate_multi_list_box(options):
        """
        Generates a Multi List Box, consisting of scrollable columns and rows
        :param options: A dictionary following the scheme {titles: [list], types: [list]}
        :return: A dictionary with the individual parts of the multi list box
                    scrollable: the actual widget
                    selection: the object keeping track of the selected options
                    list_store: the ListStore object containing all options
        """
        types = tuple(options["types"])
        titles = options["titles"]

        list_store = Gtk.ListStore(*types)
        tree_view = Gtk.TreeView.new_with_model(list_store.filter_new())
        for i, column_title in enumerate(titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            tree_view.append_column(column)
        scrollable_tree_list = Gtk.ScrolledWindow()
        scrollable_tree_list.set_vexpand(True)
        scrollable_tree_list.add(tree_view)
        tree_selection = tree_view.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        scrollable_tree_list.set_hexpand(True)
        scrollable_tree_list.set_vexpand(True)
        return {"scrollable": scrollable_tree_list, "selection": tree_selection, "list_store": list_store}

    @staticmethod
    def generate_radio_button(text):
        """
        Generates a Radio Button
        :param text: the text to be displayed together with the radio button
        :return: the RadioButton object
        """
        radio = Gtk.RadioButton.new_with_label(None, text)
        return radio

    @staticmethod
    def generate_check_box(text, active=False):
        """
        Generates a Checkbox
        :param text: the text to be displayed beside the checkbox
        :param active: the default state of the checkbox
        :return: the CheckButton object
        """
        check_box = Gtk.CheckButton.new_with_label(text)
        if active:
            check_box.set_active(True)
        return check_box

    @staticmethod
    def get_current_selected_combo_box_option(combo_box_dict):
        """
        Establishes the currently selected combo box option
        :param combo_box_dict: the combo box dictionary generated by generate_combo_box
        :return: the currently selected string
        """
        combo_box = combo_box_dict["combo_box"]
        combo_box_list = combo_box_dict["list_store"]
        combo_iter = combo_box.get_active_iter()
        if combo_iter is None:
            return None
        return combo_box_list.get(combo_iter, 0)[0]

    @staticmethod
    def get_selected_multi_list_box_elements(multi_list_box):
        """
        Returns the selected elements from a multi list box
        :param multi_list_box: the multi list box dictionary
        :return: the selection as list of elements
        """
        tree_selection = multi_list_box["selection"]
        selected = []
        (model, path_list) = tree_selection.get_selected_rows()
        for path in path_list:
            tree_iter = model.get_iter(path)
            selected.append(model.get_value(tree_iter, 0))
        return selected
