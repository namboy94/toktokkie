import requests
from bs4 import BeautifulSoup

"""
Class that gets xdcc packlists from nibl.co.uk
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class NIBLGetter(object):

    """
    Constructor
    @:param searchTerm - the term for which a search should be done.
    """
    def __init__(self, searchTerm):
        self.searchTerm = searchTerm

    """
    Conducts the search and returns an array of arrays containing the pack information
    @:return the search results
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
            result = [fileNames[i].text.rsplit(" \n", 1)[0], botnames[i].text.rsplit(" ", 1)[0], packNumbers[i].text, filesizes[i].text]
            print(result)
            results.append(result)
            i += 1

        return results
