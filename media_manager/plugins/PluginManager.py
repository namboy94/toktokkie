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

try:
    from plugins.renamer.RenamerPlugin import RenamerPlugin
    from plugins.iconizer.IconizerPlugin import IconizerPlugin
    from plugins.batchdownloadmanager.BatchDownloadManagerPlugin import BatchDownloadManagerPlugin
    from plugins.media_manager.plugins.showmanager.ShowManagerPlugin import ShowManagerPlugin
except ImportError:
    from media_manager.plugins.renamer.RenamerPlugin import RenamerPlugin
    from media_manager.plugins.iconizer.IconizerPlugin import IconizerPlugin
    from media_manager.plugins.batchdownloadmanager.BatchDownloadManagerPlugin import BatchDownloadManagerPlugin
    from media_manager.plugins.showmanager.ShowManagerPlugin import ShowManagerPlugin


class PluginManager(object):
    """
    Class that manages plugins and checks which plugins to run
    """

    def __init__(self, config: dict) -> None:
        """
        Constructor
        Already checks which plugins to use
        :param config: the config file's [plugin] section as a dictionary
        """
        all_plugins = [RenamerPlugin(),
                       IconizerPlugin(),
                       BatchDownloadManagerPlugin(),
                       ShowManagerPlugin()]
        # New Plugins here

        self.active_plugins = []
        for plugin in all_plugins:
            if config[plugin.get_config_tag()].lower() in ["true", "yes", "1"]:
                self.active_plugins.append(plugin)

    def get_plugins(self) -> list:
        """
        Returns a list of plugins, which should be used by the user interface. (CLI or GUI)
        :return: the list of plugins
        """
        return self.active_plugins
