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

from plugins.genericPlugin.userinterfaces.GenericCLI import GenericCLI
from plugins.renamer.utils.Renamer import Renamer

"""
CLI for the Renamer plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class RenamerCLI(GenericCLI):

    """
    Constructor
    @:param directory - used if only a single directory is used
    """
    def __init__(self):
        print()

    """
    Starts the CLI, or renames the originally given directory and exits
    """
    def start(self):
        while True:
            userInput = input("Enter the absolute file path of the folder to be used for renaming")
            if userInput.lower() in ["exit", "quit"]: break
            self.renameLoop(userInput)

    """
    """
    def renameLoop(self, directory):
        renamer = Renamer(directory)
        confirmation = renamer.requestConfirmation()
        if self.confirmer(confirmation):
            renamer.confirm(confirmation)
            renamer.startRename()

    """
    """
    def confirmer(self, confirmation):
        print("Confirmation:")
        i = 0
        while i < len(confirmation[0]):
            print("\nrename")
            print(confirmation[0][i])
            print("to")
            print(confirmation[1][i])
            print("?")
            answer = ""
            while not answer.lower() in ["y", "n"]:
                answer = input("(y/n)")
                if answer == "n": return False
            i += 1
        return True