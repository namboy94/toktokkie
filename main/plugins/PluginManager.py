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

from plugins.renamer.RenamerPlugin import RenamerPlugin
from plugins.xdccSearchAndDownload.XDCCPlugin import XDCCPlugin
from plugins.iconizer.IconizerPlugin import IconizerPlugin
from plugins.batchDownloadManager.BatchDownloadManagerPlugin import BatchDownloadManagerPlugin

"""
Class that manages plugins and checks which plugins to run
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class PluginManager(object):

    """
    Constructor
    Already checks which plugins to use
    @:param config - the config file's [plugin] section as a dictionary
    """
    def __init__(self, config):
        allPlugins = []
        allPlugins.append(RenamerPlugin())
        allPlugins.append(XDCCPlugin())
        allPlugins.append(IconizerPlugin())
        allPlugins.append(BatchDownloadManagerPlugin())
        #New Plugins here

        #overrides reading from config
        self.activePlugins = allPlugins
        """
        self.activePlugins = []
        for plugin in allPlugins:
            if config[plugin.getConfigTag()].lower() in ["true", "yes", "1"]:
                self.activePlugins.append(plugin)
        """

    """
    Returns a list of plugins, which should be used by the user interface. (CLI or GUI)
    """
    def getPlugins(self):
        return self.activePlugins