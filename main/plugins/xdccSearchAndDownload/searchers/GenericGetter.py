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
Class that defines interfaces for modules that search xdcc packlists
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class GenericGetter(object):

    """
    Constructor
    @:param searchTerm - the term for which a search should be done.
    """
    def __init__(self, searchTerm):
        self.searchTerm = searchTerm

    """
    Conducts the search
    @:return the search results as a list of XDCCPack objects
    """
    def search(self):
        raise NotImplementedError()

    """
    Checks to which server a given bot belongs to.
    @:param bot - the bot's name to be used
    @:return the server name
    """
    def getServer(self, bot):
        return "irc.rizon.net"

    """
    Checks to which channel a given bot belongs to
    @:param bot - the bot to check for
    @:return the channel
    """
    def getChannel(self, bot):
        if bot == "E-D|Mashiro":
            return "exiled-destiny"
        return "intel"