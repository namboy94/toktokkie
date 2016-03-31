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

# imports
import sys


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

    def start(self):
        """
        Starts the CLI
        """
        raise NotImplementedError()

    def stop(self):
        """
        Ends the CLI and restarts the parent CLI, or exits with code 0 if no parent was defined
        """
        if self.parent is not None:
            self.parent.start()
        else:
            sys.exit(0)
