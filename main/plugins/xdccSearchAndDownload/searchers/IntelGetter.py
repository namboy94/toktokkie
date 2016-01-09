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