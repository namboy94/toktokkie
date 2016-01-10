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