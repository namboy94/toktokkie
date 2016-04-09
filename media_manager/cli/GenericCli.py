"""
LICENSE:

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

LICENSE
"""

# imports
# noinspection PyUnresolvedReferences
import readline
import sys

try:
    from cli.exceptions.ReturnException import ReturnException
except ImportError:
    from media_manager.cli.exceptions.ReturnException import ReturnException


class GenericCli(object):
    """
    Class that defines some behaviour of the CLI
    """

    def __init__(self, parent=None) -> None:
        """
        Constructor
        :param parent: The parent CLI to which the CLI can return to
        :return: void
        """
        self.parent = parent

    def start(self, title=None):
        """
        Starts the CLI
        :param title: Title text shown once
        :return: void
        """
        try:
            if title is not None:
                print(title)
            while True:
                self.mainloop()
        except ReturnException:
            print()
            self.stop()

    def stop(self):
        """
        Ends the CLI and restarts the parent CLI, or exits with code 0 if no parent was defined
        :return: void
        """
        if self.parent is not None:
            self.parent.start()
        else:
            sys.exit(0)

    def mainloop(self):
        """
        The main loop of the CLI
        :return: void
        """
        raise NotImplementedError()

    @staticmethod
    def ask_user(message=None, default=None):
        """
        Creates a user prompt with default behaviours, reducing code reuse
        :param message: Message to be displayed to the user
        :param default: Default value if only enter/return is pressed
        """
        if default is None:
            prompt_message = message
        else:
            prompt_message = message + "[" + default + "]"

        if message is not None:
            user_response = input(prompt_message)
        else:
            user_response = input("\n")
        if user_response.lower() in ["quit", "return", "exit"]:
            raise ReturnException
        elif user_response == "" and default is not None:
            return default
        else:
            return user_response
