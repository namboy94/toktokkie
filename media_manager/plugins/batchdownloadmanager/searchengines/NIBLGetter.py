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

# imports
import requests
from bs4 import BeautifulSoup

try:
    from plugins.batchdownloadmanager.searchengines.GenericGetter import GenericGetter
    from plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack
except ImportError:
    from media_manager.plugins.batchdownloadmanager.searchengines.GenericGetter import GenericGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack


class NIBLGetter(GenericGetter):
    """
    Class that searches the xdcc pack lists from nibl.co.uk
    """

    def search(self):
        """
        Method that conducts the xdcc pack search

        :return: the search results as a list of XDCCPack objects
        """
        split_search_term = self.search_term.split(" ")
        prepared_search_term = split_search_term[0]
        i = 1
        while i < len(split_search_term):
            prepared_search_term += "+" + split_search_term[i]
            i += 1

        url = "http://nibl.co.uk/bots.php?search=" + prepared_search_term
        content = BeautifulSoup(requests.get(url).text, "html.parser")
        file_names = content.select(".filename")
        pack_numbers = content.select(".packnumber")
        bot_names = content.select(".botname")
        file_sizes = content.select(".filesize")

        results = []

        i = 0
        while i < len(file_names):
            filename = file_names[i].text.rsplit(" \n", 1)[0]
            bot = bot_names[i].text.rsplit(" ", 1)[0]
            server = self.get_server(bot)
            channel = self.get_channel(bot)
            packnumber = int(pack_numbers[i].text)
            size = file_sizes[i].text
            result = XDCCPack(filename, server, channel, bot, packnumber, size)
            results.append(result)
            i += 1

        return results

    def get_server(self, bot: str) -> str:
        """
        Checks to which server a given xdcc-serving bot belongs to.

        :param bot: the bot to check the server name for
        :return: the server name
        """

        if bot == "HelloKitty" or "CR-" in bot:
            return "#horriblesubs"
        elif bot == "E-D|Mashiro":
            return "#exiled-destiny"
        else:
            return "#intel"

    def get_channel(self, bot: str) -> str:
        """
        Checks to which channel a given xdcc-serving bot belongs to

        :param bot: the bot to check the channel name for
        :return: the channel name
        """
        return "irc.rizon.net"
