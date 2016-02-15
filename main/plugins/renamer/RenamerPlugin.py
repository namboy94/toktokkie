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

from plugins.common.GenericPlugin import GenericPlugin
from plugins.renamer.userinterface.RenamerCLI import RenamerCLI
from plugins.renamer.userinterface.RenamerGUI import RenamerGUI

"""
Class that handles renaming of episodes
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class RenamerPlugin(GenericPlugin):

    """
    @:return "Renamer"
    """
    def getName(self):
        return "Renamer"

    """
    @:return "renamer"
    """
    def getConfigTag(self):
        return "renamer"

    """
    @:return "renamer"
    """
    def getCommandName(self):
        return "renamer"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        RenamerCLI().start()

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        RenamerGUI(parentGUI, "Renamer").start()