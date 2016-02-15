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

from plugins.genericPlugin.GenericPlugin import GenericPlugin
from plugins.xdccSearchAndDownload.userinterfaces.XDCCGUI import XDCCGUI
from plugins.xdccSearchAndDownload.userinterfaces.XDCCCLI import XDCCCLI

"""
Class that handles renaming of episodes
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class XDCCPlugin(GenericPlugin):

    """
    @:return "XDCC-Search-Download"
    """
    def getName(self):
        return "XDCC-Search-Download"

    """
    @:return "xdcc-searchdownload"
    """
    def getConfigTag(self):
        return "xdcc-searchdownload"

    """
    @:return "xdcc-searchdl"
    """
    def getCommandName(self):
        return "xdcc-searchdl"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        XDCCCLI().start()

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        XDCCGUI(parentGUI, "XDCC Search and Download").start()
