"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

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
import urwid
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager


class TVSeriesRenamerUrwidTui(object):
    """
    Urwid TUI for the TV Series Renamer functionality
    """

    def __init__(self) -> None:
        """
        Initializes the CLI's various local variables
        """

        title = urwid.Text("TV Episode Renamer")
        div = urwid.Divider()

        dir_entry_text = urwid.Text("Directory:")
        self.dir_entry = urwid.Edit()
        self.dir_entry.set_edit_text(os.getcwd())
        self.recursive_check = urwid.CheckBox("Recursive?")

        naming_scheme_text = urwid.Text("Naming Scheme:")
        self.renaming_schemes = []

        for scheme in SchemeManager.get_scheme_names() + ["Test"]:
            urwid.RadioButton(group=self.renaming_schemes, label=scheme)

        episodes_text = urwid.Text("Episodes:")

        confirm_button = urwid.Button("Confirm")

        self.body = [title, div, dir_entry_text, self.dir_entry, self.recursive_check, div, naming_scheme_text]
        self.body += self.renaming_schemes + [div, episodes_text, div, confirm_button]

        box = urwid.ListBox(urwid.SimpleFocusListWalker(self.body))
        padding = urwid.Padding(box, left=2, right=2)

        self.top = urwid.Overlay(padding, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 80),
                                 valign='middle', height=('relative', 70),
                                 min_width=20, min_height=10)

    def start(self) -> None:
        """
        Starts the TUI

        :return: None
        """
        urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')]).run()
