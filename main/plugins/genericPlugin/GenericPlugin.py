"""
Generic Plugin that serves as a unified interface for the plugins.
@author Hermann Krumrey <hermann@krumreyh.com>
"""
class GenericPlugin(object):

    """
    @:return the name of this plugin
    """
    def getName(self):
        raise NotImplementedError()

    """
    Starts the CLI of the plugin
    """
    def startCLI(self, parentCLI):
        raise NotImplementedError()

    """
    Starts the GUI of the plugin
    """
    def startGUI(self, parentGUI):
        raise NotImplementedError()