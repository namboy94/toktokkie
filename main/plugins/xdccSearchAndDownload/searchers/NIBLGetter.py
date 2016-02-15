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

import requests
from bs4 import BeautifulSoup
from plugins.xdccSearchAndDownload.searchers.GenericGetter import GenericGetter
from plugins.xdccSearchAndDownload.searchers.objects.XDCCPack import XDCCPack

"""
Class that gets xdcc packlists from nibl.co.uk
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class NIBLGetter(GenericGetter):

    """
    Conducts the search
    @:return the search results as a list of XDCCPack objects
    """
    def search(self):
        splitSearchTerm = self.searchTerm.split(" ")
        preparedSearchTerm = splitSearchTerm[0]
        i = 1
        while i < len(splitSearchTerm):
            preparedSearchTerm += "+" + splitSearchTerm[i]
            i += 1

        url = "http://nibl.co.uk/bots.php?search=" + preparedSearchTerm
        content = BeautifulSoup(requests.get(url).text, "html.parser")
        fileNames = content.select(".filename")
        packNumbers = content.select(".packnumber")
        botnames = content.select(".botname")
        filesizes = content.select(".filesize")

        results = []

        i = 0
        while i < len(fileNames):
            filename = fileNames[i].text.rsplit(" \n", 1)[0]
            bot = botnames[i].text.rsplit(" ", 1)[0]
            server = self.getServer(bot)
            channel = self.getChannel(bot)
            packnumber = int(packNumbers[i].text)
            size = filesizes[i].text
            result = XDCCPack(filename, server, channel, bot, packnumber, size)
            results.append(result)
            i += 1

        return results
