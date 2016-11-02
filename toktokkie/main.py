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
from toktokkie.ui.cli.StartScreenCli import StartScreenCli
from toktokkie.ui.qt.StartPageQtGui import start as gui_start


# noinspection PyTypeChecker
def main(cli_mode: bool = False) -> None:
    """
    Main method that runs the program.

    It can be used without parameters, in which case it will start in the most appropriate
    UI mode, which is usually the QT GUI. The CLI can be used as a fallback.

    :param cli_mode: Flag that can be set to force CLI mode
    :return:         None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action="store_true", help="Starts the program in CLI mode")
    args = parser.parse_args()

    if args.c:
        cli_mode = True

    # noinspection PyBroadException
    try:
        if not cli_mode:
            try:
                gui_start()
            except Exception as e:
                raise e
                StartScreenCli().start()
        else:
            StartScreenCli().start()
    except:
        SentryLogger.sentry.captureException()
