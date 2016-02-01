"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a progam that allows convenient managing of various
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

import requests
from bs4 import BeautifulSoup
from plugins.xdccSearchAndDownload.searchers.GenericGetter import GenericGetter
from plugins.xdccSearchAndDownload.searchers.objects.XDCCPack import XDCCPack

"""
Class that gets xdcc packlists from intel.haruhichan.com
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class IntelGetter(GenericGetter):

    """
    Conducts the search
    @:return the search results as a list of XDCCPack objects
    """
    def search(self):
        splitSearchTerm = self.searchTerm.split(" ")
        preparedSearchTerm = splitSearchTerm[0]
        i = 1
        while i < len(splitSearchTerm):
            preparedSearchTerm += "%20" + splitSearchTerm[i]
            i += 1

        url = "http://intel.haruhichan.com/?s=" + preparedSearchTerm
        content = BeautifulSoup(requests.get(url).text, "html.parser")
        packs = content.select("td")

        results = []

        i = 0
        filename = ""
        bot = ""
        server = ""
        channel = ""
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
                channel = self.getChannel(bot)
                server = self.getServer(bot)
                result = XDCCPack(filename, server, channel, bot, packnumber, size)
                results.append(result)
            i += 1

        return results