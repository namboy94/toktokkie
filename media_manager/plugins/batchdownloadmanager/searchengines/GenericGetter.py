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


class GenericGetter(object):
    """
    Class that defines interfaces for modules that search xdcc pack lists
    """

    def __init__(self, search_term):
        """
        Constructor
        :param: search_term: the term for which a search should be done.
        """
        self.search_term = search_term

    def search(self):
        """
        Conducts the search
        :return: the search results as a list of XDCCPack objects
        """
        raise NotImplementedError()

    def get_server(self, bot):
        """
        Checks to which server a given bot belongs to.
        :param bot: the bot's name to be used
        :return: the server name
        """
        raise NotImplementedError()

    def get_channel(self, bot):
        """
        Checks to which channel a given bot belongs to
        :param bot: the bot to check for
        :return: the channel
        """
        raise NotImplementedError()