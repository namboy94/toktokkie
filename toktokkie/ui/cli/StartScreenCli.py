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

# import
import curses
import _curses
import toktokkie.metadata as metadata


class StartScreenCli(object):
    """
    A Curses CLI that shows a list of available functions to select from
    """

    def __init__(self) -> None:
        """
        Initializes the CLI's local variables
        """
        # Initialize Curses, since we're not using the wrapper()
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)

        self.screen.keypad(True)
        self.cursor_location = 0

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        self.gpl_notice = ["Tok Tokkie Media Manager V" + metadata.version_number,
                           "Copyright (C) 2015,2016 Hermann Krumrey",
                           "",
                           "This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.",
                           "This is free software, and you are welcome to redistribute it",
                           "under certain conditions; type `show c' for details."]

        self.selection = {"TV Series Renamer": None,
                          "TV Series Manager": None,
                          "Folder Iconizer": None,
                          "XDCC Downloader": None,
                          "XDCC Download Manager": None,
                          "Manga Downloader": None,
                          "Manga Download Manager": None}

        self.selection_indices = {}

    def end(self) -> None:
        """
        Ends the CLI, and resets the terminal to a sane state

        :return: None
        """
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def start(self) -> None:
        """
        Starts the CLI

        :return: None
        """
        try:
            for line in self.gpl_notice:
                self.screen.addstr(self.cursor_location, 0, line)
                self.cursor_location += 1
            self.cursor_location += 1

            for element in self.selection:
                self.screen.addstr(self.cursor_location, 0, element)
                self.selection_indices[self.cursor_location] = element
                self.cursor_location += 1
            self.cursor_location = min(self.selection_indices)

            self.screen.addstr(self.cursor_location, 0, self.selection_indices[self.cursor_location],
                               curses.color_pair(1))
            self.handle_user_input()
        except _curses.error:
            self.end()
            print("Terminal too small to display the CLI")
        except Exception as e:
            self.end()
            raise e

    def handle_user_input(self) -> None:
        """
        Handles the continuous user input

        :return: None
        """
        try:
            while True:
                keypress = self.screen.getch()

                if keypress == curses.KEY_UP and self.cursor_location > min(self.selection_indices):
                    self.move_selection_cursor(up=True)
                elif keypress == curses.KEY_DOWN and self.cursor_location < max(self.selection_indices):
                    self.move_selection_cursor(down=True)
                elif keypress == curses.KEY_ENTER or keypress == 10:
                    selected = self.selection[self.selection_indices[self.cursor_location]]
                    if selected is not None:
                        self.end()
                        # noinspection PyCallingNonCallable
                        selected().start()
                        break
        except KeyboardInterrupt:
            self.end()
            print("Thanks for using the Tok Tokkie Media Manager!")

    def move_selection_cursor(self, up: bool = False, down: bool = False) -> None:
        """
        Moves the visible cursor up or down the list of selection entries
        Only one of the parameters my be True (the same goes for False),
        otherwise this method returns without doing anything

        :param up:   move the cursor up one entry
        :param down: move the cursor down one entry
        :return:     None
        """
        if (up and down) or (not up and not down):
            return

        self.screen.addstr(self.cursor_location, 0, self.selection_indices[self.cursor_location], curses.color_pair(0))
        self.cursor_location = self.cursor_location - 1 if up else self.cursor_location + 1
        self.screen.addstr(self.cursor_location, 0, self.selection_indices[self.cursor_location], curses.color_pair(1))
