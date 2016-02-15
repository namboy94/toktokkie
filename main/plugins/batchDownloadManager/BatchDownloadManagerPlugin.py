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

from plugins.batchDownloadManager.userinterfaces.BatchDownloadManagerCLI import BatchDownloadManagerCLI

from plugins.batchDownloadManager.userinterfaces.BatchDownloadManagerGUI import BatchDownloadManagerGUI
from plugins.common.GenericPlugin import GenericPlugin

"""
Class that handles the calls to the BatchDownloadManager
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class BatchDownloadManagerPlugin(GenericPlugin):

    """
    @:return "Batch Download Manager"
    """
    def getName(self):
        return "Batch Download Manager"

    """
    @:return "batch-download"
    """
    def getConfigTag(self):
        return "batch-download"

    """
    @:return "batch download"
    """
    def getCommandName(self):
        return "batch download"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        BatchDownloadManagerCLI().start()

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        BatchDownloadManagerGUI(parentGUI, "Batch Download Manager").start()
