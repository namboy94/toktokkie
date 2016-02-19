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
    from media_manager.plugins.common.GenericPlugin import GenericPlugin
except ImportError:
    from plugins.common.GenericPlugin import GenericPlugin

try:
    from media_manager.plugins.iconizer.userinterfaces.IconizerGUI import IconizerGUI as PluginGui
except ImportError:
    try:
        from media_manager.plugins.iconizer.userinterfaces.IconizerTkGui import IconizerTkGui as PluginGui
    except ImportError:
        try:
            from plugins.iconizer.userinterfaces.IconizerGUI import IconizerGUI as PluginGui
        except ImportError:
            from plugins.iconizer.userinterfaces.IconizerTkGui import IconizerTkGui as PluginGui


class IconizerPlugin(GenericPlugin):
    """
    Class that handles iconizing of folders
    """

    def get_name(self):
        """
        :return "Iconizer"
        """
        return "Iconizer"

    def get_config_tag(self):
        """
        :return "iconizer"
        """
        return "iconizer"

    def get_command_name(self):
        """
        :return "iconizer"
        """
        return "iconizer"

    def start_gui(self, parent_gui):
        """
        Starts the GUI, while hiding the parent until finished
        :param parent_gui: the parent window
        :return void
        """
        PluginGui(parent_gui).start()