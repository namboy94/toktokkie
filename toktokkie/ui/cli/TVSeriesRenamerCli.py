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
import curses
from toktokkie.ui.cli.CursesCli import CursesCli
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager


class TVSeriesRenamerCli(CursesCli):
    """
    CLI for the TV Series Renamer functionality.
    """

    def __init__(self) -> None:
        """
        Initializes the CLI's various local variables
        """
        super().__init__()
        self.directory_path_edit = os.getcwd()
        self.recursive_selected = False
        self.selected_naming_scheme = None
        self.confirmations = []
        self.renamer = None

    def start(self) -> None:
        """
        Starts the CLI

        :return: None
        """
        self.draw()
        self.cursor_location = min(self.selectable_values)
        self.draw()
        self.handle_user_input()
        super().start()

    def draw(self) -> None:
        """
        Redraws the screen with the current program state

        :return: None
        """
        self.selectable_values = {}
        previous_cursor_location = self.cursor_location

        self.screen.clear()
        self.cursor_location = 0

        self.print("TV Series Renamer")
        self.print("")

        self.print("Directory:")
        self.print(self.directory_path_edit.ljust(30), True)

        recursive_color = 2 if not self.recursive_selected else 3
        self.screen.addstr(self.cursor_location, 0, "Recursive?", curses.color_pair(recursive_color))
        self.selectable_values[self.cursor_location] = "Recursive?"
        self.cursor_location += 1

        self.print("")
        self.print("Naming Scheme:")

        for scheme in SchemeManager.get_scheme_names():

            if scheme == self.selected_naming_scheme or self.selected_naming_scheme is None:
                self.screen.addstr(self.cursor_location, 0, scheme, curses.color_pair(3))
                self.selectable_values[self.cursor_location] = scheme
                self.cursor_location += 1

                self.selected_naming_scheme = scheme

            else:
                self.print(scheme, True)

        self.print("")
        self.print("Episodes:")

        self.print("")
        self.print("Confirm", True)

        try:
            self.screen.addstr(previous_cursor_location, 0,
                               self.selectable_values[previous_cursor_location], curses.color_pair(1))
            self.cursor_location = previous_cursor_location
        except KeyError:
            pass

        self.screen.refresh()

    def handle_user_input(self) -> None:
        """
        Handles the continuous user input

        :return: None
        """
        while True:
            keypress = self.screen.getch()

            if not self.handle_up_down_selection(keypress):
                if keypress == curses.KEY_ENTER or keypress == 10:
                    selected = self.selectable_values[self.cursor_location]

                    if selected == "Recursive?":
                        self.recursive_selected = not self.recursive_selected
            self.draw()
