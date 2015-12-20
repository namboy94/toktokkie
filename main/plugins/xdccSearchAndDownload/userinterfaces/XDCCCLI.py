from plugins.genericPlugin.userinterfaces.GenericCLI import GenericCLI
from plugins.common.onlineDataGetters.NIBLGetter import NIBLGetter
from plugins.xdccSearchAndDownload.downloaders.TwistedDownloader import TwistedDownloader

"""
CLI for the XDCC Search and Download plugin
@author Hermann Krumrey <hermann@krumreyh.com>
"""
class XDCCCLI(GenericCLI):

    """
    Constructor
    """
    def __init__(self):
        print()

    """
    Starts the CLi
    """
    def start(self):
        print("Renamer Plugin Started")
        searchTerm = input("Enter the search term to search for")
        results = NIBLGetter(searchTerm).search()
        print("Results:\n")
        i = 1
        for result in results:
            print(str(i) + result.toString())
            i += 1
        choicesString = input("\nChoose any number of search results to download by typing the index of each desired "
                        "search result, seperated by commas.")
        choices = choicesString.split(",")
        packs = []
        for choice in choices:
            packs.append(results[int(choice) - 1])
        TwistedDownloader(packs).downloadLoop()