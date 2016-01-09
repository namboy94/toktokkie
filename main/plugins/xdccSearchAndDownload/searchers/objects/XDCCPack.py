"""
Class that models an XDCC Pack Object
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class XDCCPack(object):

    """
    Constructor
    """
    def __init__(self, filename, server, channel, bot, packnumber, size):
        self.filename = filename
        self.server = server
        self.channel = channel
        self.bot = bot
        self.packnumber = packnumber
        self.size = size

    """
    Returns the bot information as a string
    @:return the bot information
    """
    def toString(self):
        return self.filename + "  -  " + self.bot + "  -  Size:" + self.size

    """
    Returns the bot information as a tuple
    @:return the bot information
    """
    def toTuple(self):
        return (self.bot, self.packnumber, self.size, self.filename)