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
Class that models an XDCC Pack Object
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class XDCCPack(object):

    """
    Constructor
    """
    def __init__(self, filename, server, channel, bot, packnumber, size):
        self.filename = filename
        self.server = server
        self.channel = channel
        self.bot = bot
        self.packnumber = packnumber
        self.size = size

    """
    Returns the bot information as a string
    @:return the bot information
    """
    def toString(self):
        return self.filename + "  -  " + self.bot + "  -  Size:" + self.size

    """
    Returns the bot information as a tuple
    @:return the bot information
    """
    def toTuple(self):
        return (self.bot, self.packnumber, self.size, self.filename)