"""
Generic CLI class defining a kind of interface for CLI construction
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class GenericCLI(object):

    """
    Starts the CLI
    """
    def start(self):
        raise NotImplementedError("CLI not implemented correctly")