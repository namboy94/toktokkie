"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
import time
import urwid
from threading import Thread
from toktokkie.utils.iconizing.Iconizer import Iconizer


class FolderIconizerUrwidTui(object):
    """
    Urwid TUI for the Directory Iconizing functionality
    """

    def __init__(self) -> None:
        """
        Initializes the TUI's various widgets
        """
        self.iconizer = Iconizer()

        self.iconizing = False

        self.top = None
        self.loop = None
        self.body = []
        self.list_walker = None

        self.title = urwid.Text("Folder Iconizer")

        self.directory_text = urwid.Text("Directory:")
        self.directory_edit = urwid.Edit()
        self.directory_edit.set_edit_text(os.getcwd())

        self.recursive_check = urwid.CheckBox("Recursive?")

        self.iconize_button = urwid.Button("Iconize")
        urwid.connect_signal(self.iconize_button, 'click', self.iconize)

        self.pop_up_button = urwid.Button("OK")
        urwid.connect_signal(self.pop_up_button, 'click', self.reset_ui)

        self.lay_out()

    def lay_out(self) -> None:
        """
        Handles the layout of the TUI elements

        :return: None
        """
        div = urwid.Divider()

        directory_edit = urwid.AttrMap(self.directory_edit, None, focus_map='reversed')
        iconize_button = urwid.AttrMap(self.iconize_button, None, focus_map='reversed')

        self.body = [self.title, div, self.directory_text, directory_edit,
                     div, self.recursive_check, div, iconize_button]

        self.list_walker = urwid.SimpleFocusListWalker(self.body)
        self.top = urwid.Overlay(urwid.Padding(urwid.ListBox(self.list_walker), left=2, right=2),
                                 urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 80),
                                 valign='middle', height=('relative', 70),
                                 min_width=20, min_height=10)

    def start(self) -> None:  # pragma: no cover
        """
        Starts the TUI

        :return: None
        """
        self.loop = urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')])
        self.loop.run()
        self.iconizing = False

    # noinspection PyUnusedLocal
    def iconize(self, iconize_button: urwid.Button, parameters: None = None) -> None:
        """
        Starts the iconization

        :param iconize_button: The button that called this method
        :param parameters:     The parameters given, will not be used
        :return:               None
        """
        self.iconizing = True
        self.start_spinner()
        directory = self.directory_edit.get_edit_text()

        if self.recursive_check.get_state():
            self.iconizer.recursive_iconize(directory)
        else:
            self.iconizer.iconize_directory(directory)
        self.iconizing = False

        text = urwid.Text("Iconization has completed")

        self.list_walker[:] = [text, self.pop_up_button]
        self.loop.draw_screen()

    def start_spinner(self):
        """
        Starts a little animation on the iconizer button to indicate that the iconization is running

        :return: None
        """
        def spinner():
            while self.iconizing:
                new_text = "Iconizing" + (self.iconize_button.get_label().count(".") % 3 + 1) * "."
                self.iconize_button.set_label(new_text)
                self.loop.draw_screen()
                time.sleep(0.3)

            self.iconize_button.set_label("Start")
            self.loop.draw_screen()
        Thread(target=spinner).start()

    # noinspection PyUnusedLocal
    def reset_ui(self, button: urwid.Button) -> None:
        """
        Restores the UI after a message popup was shown

        :param button: The button calling this method
        :return:       None
        """
        self.list_walker[:] = self.body
        self.loop.draw_screen()

    def quit(self) -> None:
        """
        Cleans up any variables that may cause thread to continue executing after the TUI ends

        :return: None
        """
        self.iconizing = False
