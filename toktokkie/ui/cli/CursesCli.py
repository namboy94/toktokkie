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
import curses
from typing import Iterable


class CursesCli(object):
    """
    A generic Curses CLI that reduces code reuse
    """

    def __init__(self) -> None:
        """
        Initializes basic curses options, similar to how curses.wrapper does it
        """

        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)

        self.screen.keypad(True)
        self.cursor_location = 0

        self.selectable_values = {}

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Selected Color
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)     # Unmarked Color
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)   # Marked Color

        self.screen.clear()

    def start(self) -> None:
        """
        Starts the CLI

        :return: None
        """
        raise NotImplementedError()

    def end(self) -> None:
        """
        Ends the CLI, and resets the terminal to a sane state

        :return: None
        """
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def print_iterable(self, iterable: Iterable[str]) -> None:
        """
        Prints an iterable object like a list to the console at the current cursor
        position and moves the cursor accordingly
        At the end, the cursor is on the line directly after this list

        :param iterable: The iterable object to use
        :return:         None
        """
        for item in iterable:
            self.screen.addstr(self.cursor_location, 0, item)
            self.cursor_location += 1

    def print(self, string: str, selectable: bool = False) -> None:
        """
        Prints a simple string at the current cursor location.
        Increments the cursor location afterwards

        :param string: the string to print
        :param selectable: Can be selected by using the arrow keys
        :return: None
        """
        self.screen.addstr(self.cursor_location, 0, string)
        if selectable:
            self.selectable_values[self.cursor_location] = string
        self.cursor_location += 1

    def handle_up_down_selection(self, keypress: int) -> bool:
        """
        Handles up/down arrow key presses meant to go up or down in a selection

        :param keypress: the key press
        :return:         if the keypress was either up, or down, the Tue, False otherwise
        """

        if keypress not in [curses.KEY_DOWN, curses.KEY_UP]:
            return False

        try:
            self.screen.addstr(self.cursor_location, 0,
                               self.selectable_values[self.cursor_location], curses.color_pair(0))
        except KeyError:
            pass

        if keypress == curses.KEY_UP and not self.cursor_location == min(self.selectable_values):
            self.cursor_location -= 1
            while self.cursor_location not in self.selectable_values:
                self.cursor_location -= 1
        elif keypress == curses.KEY_DOWN and not self.cursor_location == max(self.selectable_values):
            self.cursor_location += 1
            while self.cursor_location not in self.selectable_values:
                self.cursor_location += 1

        try:
            self.screen.addstr(self.cursor_location, 0,
                               self.selectable_values[self.cursor_location], curses.color_pair(1))
        except KeyError:
            pass

        return True
