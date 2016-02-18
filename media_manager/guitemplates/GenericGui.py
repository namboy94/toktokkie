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


class GenericGui(object):
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
        dummy = (title, parent, hide_parent)
        dummy += (1,)
        raise NotImplementedError()

    def lay_out(self):
        """
        Abstract method that adds objects to the GUI and places them into the layout.
        :raise NotImplementedError to indicate that this class is abstract
        :return: void
        """
        raise NotImplementedError()

    def start(self):
        """
        Starts the GUI and enters the gui mainloop. If this window has a parent,
        it will be hidden during the mainloop and reappear at the end
        :return: void
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    def show_message_dialog(self, primary_message, secondary_message=""):
        """
        Opens a message box displaying a primary and a secondary message
        :param primary_message: the primary message to be displayed
        :param secondary_message: the secondary message to be displayed
        :return: void
        """
        raise NotImplementedError()

    def show_y_n_dialog(self, primary_message, secondary_message=""):
        """
        Opens a yes/no dialog
        :param primary_message: the primary message to be displayed
        :param secondary_message: the secondary message to be displayed
        :return: True, if yes was selected, False otherwise
        """
        raise NotImplementedError()

    def show_file_chooser_dialog(self):
        """
        Creates a file chooser dialog
        :return: the selected file path
        """
        raise NotImplementedError()

    def show_text_box(self, message):
        """
        Shows a text box and retrieves a value entered by the user
        :param message: The message addressed to the user to be displayed
        :return: the entered string
        """
        raise NotImplementedError()

    def show_password_box(self, message):
        """
        Shows a text box asking for a password and return the password
        :param message: The message addressed to the user to be displayed
        :return: the password
        """
        raise NotImplementedError()

    @staticmethod
    def generate_label(label_text):
        """
        Generates a GTK Label
        :param label_text: the text to be displayed on the label
        :return: the Label object
        """
        raise NotImplementedError()

    @staticmethod
    def generate_simple_button(button_text, command, *additional_args):
        """
        Generates a GTK Button
        :param button_text: the text to be displayed on the button
        :param command: the command to be executed when pressing this button
        :param additional_args: additional arguments to be passed to the command
        :return: the Button object
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    @staticmethod
    def generate_combo_box(options):
        """
        Generates a combo box with a given amount of options
        :param options: a list of (string) options to be displayed
        :return: a dictionary with the individual parts of the combo box
                    combo_box: the Combo Box object
                    list_store: the ListStore object that stores the options for the combo box
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    @staticmethod
    def generate_radio_button(text):
        """
        Generates a Radio Button
        :param text: the text to be displayed together with the radio button
        :return: the RadioButton object
        """
        raise NotImplementedError()

    @staticmethod
    def generate_check_box(text, active=False):
        """
        Generates a Checkbox
        :param text: the text to be displayed beside the checkbox
        :param active: the default state of the checkbox
        :return: the CheckButton object
        """
        raise NotImplementedError()

    @staticmethod
    def get_current_selected_combo_box_option(combo_box_dict):
        """
        Establishes the currently selected combo box option
        :param combo_box_dict: the combo box dictionary generated by generate_combo_box
        :return: the currently selected string
        """
        raise NotImplementedError()

    @staticmethod
    def get_selected_multi_list_box_elements(multi_list_box):
        """
        Returns the selected elements from a multi list box
        :param multi_list_box: the multi list box dictionary
        :return: the selection as list of elements
        """
        raise NotImplementedError()
