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
from toktokkie.metadata import General
from toktokkie.ui.cli.CursesCli import CursesCli
from toktokkie.ui.cli.TVSeriesRenamerCli import TVSeriesRenamerCli


class StartScreenCli(CursesCli):
    """
    A Curses CLI that shows a list of available functions to select from
    """

    def __init__(self) -> None:
        """
        Initializes the CLI's local variables
        """
        super().__init__()

        self.gpl_notice = ["Tok Tokkie Media Manager V" + General.version_number,
                           "Copyright (C) 2015,2016 Hermann Krumrey",
                           "",
                           "This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.",
                           "This is free software, and you are welcome to redistribute it",
                           "under certain conditions; type `show c' for details."]

        self.selection = {"TV Series Renamer            ": TVSeriesRenamerCli,
                          "TV Series Manager            ": None,
                          "Folder Iconizer              ": None,
                          "XDCC Downloader              ": None,
                          "XDCC Download Manager        ": None,
                          "Manga Downloader             ": None,
                          "Manga Download Manager       ": None}

    def start(self) -> None:
        """
        Starts the CLI

        :return: None
        """
        message = ""
        try:
            self.print_iterable(self.gpl_notice)
            self.cursor_location += 1

            for element in sorted(self.selection):
                self.screen.addstr(self.cursor_location, 0, element)
                self.selectable_values[self.cursor_location] = element
                self.cursor_location += 1

            self.cursor_location = min(self.selectable_values)

            self.screen.addstr(self.cursor_location, 0, self.selectable_values[self.cursor_location],
                               curses.color_pair(1))
            self.handle_user_input()
        except _curses.error:
            message = "Terminal too small to display the CLI"
        except KeyboardInterrupt:
            message = "Thank you for using the Tok Tokkie Media Manager!"
        except Exception as e:
            message = e
        self.end()
        print(message)

    def handle_user_input(self) -> None:
        """
        Handles the continuous user input

        :return: None
        """
        while True:
            keypress = self.screen.getch()

            if not self.handle_up_down_selection(keypress):
                if keypress == curses.KEY_ENTER or keypress == 10:
                    selected = self.selection[self.selectable_values[self.cursor_location]]
                    if selected is not None:
                        # noinspection PyCallingNonCallable
                        selected().start()
                        break
