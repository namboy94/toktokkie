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
Class that gets xdcc packlists from ixirc.com
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class IxIRCGetter(GenericGetter):

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

        numberOfPages = 1


        baseUrl = "https://ixirc.com/?q=" + preparedSearchTerm
        content = BeautifulSoup(requests.get(baseUrl).text, "html.parser")
        pageAnalysis = content.select("h3")

        if "Over" in pageAnalysis[0].text:
            numberOfPages = 2

        analysing = False
        if numberOfPages == 2: analysing = True
        while analysing:
            url = "https://ixirc.com/?q=" + preparedSearchTerm + "&pn=" + str(numberOfPages - 1)
            content = BeautifulSoup(requests.get(url).text, "html.parser")
            pageAnalysis = content.select("h3")
            if "Over" in pageAnalysis[0].text:
                numberOfPages += 1
                continue
            else:
                analysing = False

        i = 1
        urls = [baseUrl]
        while i < numberOfPages:
            urls.append("https://ixirc.com/?q=" + preparedSearchTerm + "&pn=" + str(i))
            i += 1

        results = []

        for url in urls:
            content = BeautifulSoup(requests.get(url).text, "html.parser")
            packs = content.select("td")
            self.__getPageResults__(packs, results)

        return results

    def __getPageResults__(self, packs, results):

        filename = ""
        bot = ""
        server = ""
        channel = ""
        packnumber = 0
        size = ""

        lineCount = 0
        agoCount = 0
        aborted = False
        next = False

        for line in packs:
            if next and line.text == "": continue
            if next and not line.text == "": next = False
            if not next and line.text == "": aborted = True
            if "ago" in line.text:
                agoCount += 1
            if not aborted:
                if lineCount == 0:
                    filename = line.text
                elif lineCount == 1:
                    server = line.text
                elif lineCount == 2:
                    channel = line.text
                elif lineCount == 3:
                    bot = line.text
                elif lineCount == 4:
                    packnumber = int(line.text)
                elif lineCount == 6:
                    size = line.text
            if not aborted and agoCount == 2:
                agoCount = 0
                lineCount = 0
                next = True
                result = XDCCPack(filename, "irc." + server + ".net", channel, bot, packnumber, size)
                results.append(result)
            if aborted and agoCount == 2:
                aborted = False
                agoCount = 0
                lineCount = 0
                next = True
            if not next: lineCount += 1