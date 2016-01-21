"""
Class that defines interfaces for modules that search xdcc packlists
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class GenericGetter(object):

    """
    Constructor
    @:param searchTerm - the term for which a search should be done.
    """
    def __init__(self, searchTerm):
        self.searchTerm = searchTerm

    """
    Conducts the search
    @:return the search results as a list of XDCCPack objects
    """
    def search(self):
        raise NotImplementedError()

    """
    Checks to which server a given bot belongs to.
    @:param bot - the bot's name to be used
    @:return the server name
    """
    def getServer(self, bot):
        return "irc.rizon.net"

    """
    Checks to which channel a given bot belongs to
    @:param bot - the bot to check for
    @:return the channel
    """
    def getChannel(self, bot):
        if bot == "E-D|Mashiro":
            return "exiled-destiny"
        return "intel"