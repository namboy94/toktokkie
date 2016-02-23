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

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from functools import partial


class GenericTkGui(Tk):
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
        super().__init__()
        self.title(title)
        self.parent = parent
        self.hide_parent = hide_parent
        self.lay_out()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

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
        it will be hidden during the mainloop
        :return: void
        """
        if self.parent is not None and self.hide_parent:
            self.parent.withdraw()
        self.mainloop()

    def close_window(self):
        """
        Method run when the window closes
        :return: void
        """
        if self.parent is not None and self.hide_parent:
            self.parent.show()
        self.destroy()

    # Helper methods

    @staticmethod
    def show_message_dialog(title, message):
        """
        Opens a message box displaying a title and a message
        :param title: the title to be displayed
        :param message: the message to be displayed
        :return: void
        """
        messagebox.showinfo(title, message)

    @staticmethod
    def show_y_n_dialog(title, message):
        """
        Opens a yes/no dialog
        :param title: the title text to be displayed
        :param message: the message to be displayed
        :return: True, if yes was selected, False otherwise
        """
        if messagebox.askyesno(title, message):
            return True
        else:
            return False

    @staticmethod
    def show_file_chooser_dialog():
        """
        Creates a file chooser dialog
        :return: the selected file path
        """
        return filedialog.askopenfile()

    @staticmethod
    def show_directory_chooser_dialog():
        """
        Creates a directory chooser dialog
        :return: the selected directory path
        """
        return filedialog.askdirectory()

    @staticmethod
    def show_text_box(title, message):
        """
        Shows a text box and retrieves a value entered by the user
        :param title: The title to be displayed
        :param message: The message addressed to the user to be displayed
        :return: the entered string
        """
        return simpledialog.askstring(title, message)

    def generate_label(self, label_text):
        """
        Generates a TK Label
        :param label_text: the text to be displayed on the label
        :return: the Label object
        """
        return Label(self, text=label_text)

    def generate_image_label(self, label_image):
        """
        Generates a TK Image Label
        :param label_image: the image to be displayed on the label
        :return: the Label object
        """
        img = PhotoImage(file=label_image)
        label = Label(self, image=img)
        label.img = img
        return label

    def generate_simple_button(self, button_text, command, *additional_args):
        """
        Generates a GTK Button
        :param button_text: the text to be displayed on the button
        :param command: the command to be executed when pressing this button
        :param additional_args: additional arguments to be passed to the command
        :return: the Button object
        """
        return Button(self, text=button_text, command=partial(command, additional_args))

    def generate_text_entry(self, defaulttext="", command=None, *additional_args, change_command=None):
        """
        Generates a GTK Text Entry
        :param change_command: command run when the entry gets changed
        :param defaulttext: The text to be displayed by default
        :param command: The command to be executed if the enter key is pressed when this
                        text entry is in focus.
        :param additional_args: additional arguments to be passed to the command
        :return: the Entry object
        """
        text_var = StringVar(self, defaulttext)
        if change_command is not None:
            text_var.trace("w", lambda name, index, mode, sv=text_var: change_command(sv))
        entry = Entry(self, textvariable=text_var)
        entry.var = text_var
        if command is not None:
            entry.bind('<Return>', partial(command, additional_args))
        return entry

    def generate_combo_box(self, options):
        """
        Generates a combo box with a given amount of options
        :param options: a list of (string) options to be displayed
        :return: a dictionary with the individual parts of the combo box
                    combo_box: the Combo Box object
                    list_store: the ListStore object that stores the options for the combo box
        """
        combo_box = ttk.Combobox(self)
        combo_box['values'] = tuple(options)
        combo_box.current(0)
        combo_box.state(['readonly'])
        return combo_box

    def generate_multi_selectable_list_box(self, options):
        """
        Generates a Multiple selectable List Box
        :param options: A list of initial values
        :return:the multi selectable list box
        """
        list_box = Listbox(self, selectmode=MULTIPLE)
        for item in options:
            list_box.insert(END, item)
        return list_box

    def generate_check_box(self, text, active=False):
        """
        Generates a Checkbox
        :param text: the text to be displayed beside the checkbox
        :param active: the default state of the checkbox
        :return: the CheckButton object
        """
        var = IntVar()
        check_button = Checkbutton(self, text=text, variable=var)
        check_button.var = var
        if active:
            check_button.select()
        return check_button

    @staticmethod
    def get_selected_multi_selectable_list_box_elements(multi_selectable_list_box):
        """
        Returns the selected elements from a multi list box
        :param multi_selectable_list_box: the multi list box dictionary
        :return: the selection as list of elements
        """
        items = map(int, multi_selectable_list_box.curselection())
        selected = {}
        for item in items:
            selected[item] = (multi_selectable_list_box.get(item))
        return selected

    @staticmethod
    def clear_list_box(list_box):
        """
        Clears a list box (in-place)
        :param list_box: the list box to be cleared
        :return: void
        """
        list_box.delete(0, END)
