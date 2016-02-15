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

"""
Generic Plugin that serves as a unified interface for the plugins.
@author Hermann Krumrey <hermann@krumreyh.com>
"""
class GenericPlugin(object):

    """
    @:return the name of this plugin
    """
    def getName(self):
        raise NotImplementedError()

    """
    @:return the command that starts ths plugin
    """
    def getCommandName(self):
        raise NotImplementedError()

    """
    @:return the config tag of this plugin
    """
    def getConfigTag(self):
        raise NotImplementedError()

    """
    Starts the CLI of the plugin
    """
    def startCLI(self, parentCLI):
        raise NotImplementedError()

    """
    Starts the GUI of the plugin
    """
    def startGUI(self, parentGUI):
        raise NotImplementedError()