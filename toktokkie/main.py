#!/usr/bin/python
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
import argparse
from toktokkie.metadata import SentryLogger
from toktokkie.ui.qt.StartPageQtGui import start as gui_start
from toktokkie.ui.urwid.StartScreenUrwidTui import StartScreenUrwidTui


# noinspection PyTypeChecker
def main() -> None:
    """
    Main method that runs the program.
    The UI is determined by the arguments passed. '-g' will start the QT GUI, '-t' will start the Urwid TUI

    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tui", action="store_true", help="Starts the program in TUI mode")
    parser.add_argument("-g", "--gui", action="store_true", help="Starts the program in GUI mode")
    args = parser.parse_args()

    try:
        if args.tui:
            StartScreenUrwidTui().start()
        elif args.gui:
            gui_start()
        else:
            print("No Valid Arguments supplied")
    except KeyboardInterrupt:
        print("Thanks for using toktokkie!")
    except Exception as e:
        SentryLogger.sentry.captureException()
        raise e

if __name__ == '__main__':
    main()
