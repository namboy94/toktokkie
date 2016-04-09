"""
LICENSE:

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

LICENSE
"""

import requests
from bs4 import BeautifulSoup

try:
    from plugins.batchdownloadmanager.searchengines.GenericGetter import GenericGetter
    from plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack
except ImportError:
    from media_manager.plugins.batchdownloadmanager.searchengines.GenericGetter import GenericGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack


class IntelGetter(GenericGetter):
    """
    Class that gets xdcc pack lists from intel.haruhichan.com
    """
    
    def search(self):
        """
        Conducts the search
        :return: the search results as a list of XDCCPack objects
        """
        split_search_term = self.search_term.split(" ")
        prepared_search_term = split_search_term[0]
        i = 1
        while i < len(split_search_term):
            prepared_search_term += "%20" + split_search_term[i]
            i += 1

        url = "http://intel.haruhichan.com/?s=" + prepared_search_term
        content = BeautifulSoup(requests.get(url).text, "html.parser")
        packs = content.select("td")

        results = []

        i = 0
        bot = ""
        packnumber = ""
        size = ""
        for line in packs:
            if i % 5 == 0:
                bot = line.text
            elif (i - 1) % 5 == 0:
                packnumber = int(line.text)
            elif (i - 2) % 5 == 0:
                i += 1
                continue
            elif (i - 3) % 5 == 0:
                size = line.text
            elif (i - 4) % 5 == 0:
                filename = line.text
                channel = self.get_channel(bot)
                server = self.get_server(bot)
                result = XDCCPack(filename, server, channel, bot, packnumber, size)
                results.append(result)
            i += 1

        return results

    def get_channel(self, bot):
        """
        Gets the channel for a given bot
        :param bot: the bot
        :return: the channel
        """
        return "#intel"

    def get_server(self, bot):
        """
        Gets the server for a given bot
        :param bot: the bot
        :return: the server
        """
        return "irc.rizon.net"
